"""
Gphoto2 backend implementation

"""
import dataclasses
import logging
import time
from threading import Condition, Event

try:
    import gphoto2 as gp
except Exception as import_exc:
    raise RuntimeError("gphoto2 import error; check gphoto2 installation") from import_exc

from pymitter import EventEmitter

from photobooth.services.backends.abstractbackend import AbstractBackend, BackendStats
from photobooth.utils.stoppablethread import StoppableThread

from ...appconfig import AppConfig

logger = logging.getLogger(__name__)


class Gphoto2Backend(AbstractBackend):
    """
    The backend implementation using gphoto2
    """

    @dataclasses.dataclass
    class Gphoto2DataBytes:
        """
        bundle data bytes and it's condition.
        1) save some instance attributes and
        2) bundle as it makes sense
        """

        # jpeg data as bytes
        data: bytes = None
        # signal to producer that requesting thread is ready to be notified
        request_ready: Event = None
        # condition when frame is avail
        condition: Condition = None

    def __init__(self, evtbus: EventEmitter, config: AppConfig):
        super().__init__(evtbus, config)

        # public props (defined in abstract class also)
        self.metadata = {}

        # private props
        self._camera = gp.Camera()
        self._camera_context = gp.Context()

        self._hires_data: __class__.Gphoto2DataBytes = __class__.Gphoto2DataBytes(
            data=None, request_ready=Event(), condition=Condition()
        )

        self._lores_data: __class__.Gphoto2DataBytes = __class__.Gphoto2DataBytes(data=None, condition=Condition())

        self._camera_connected = False
        self._camera_preview_available = False
        self._count = 0
        self._fps = 0

        # worker threads
        self._generate_images_thread = StoppableThread(
            name="_generateImagesThread", target=self._generate_images_fun, daemon=True
        )
        self._stats_thread = StoppableThread(name="_statsThread", target=self._stats_fun, daemon=True)

        logger.info(f"python-gphoto2: {gp.__version__}")
        logger.info(f"libgphoto2: {gp.gp_library_version(gp.GP_VERSION_VERBOSE)}")
        logger.info(f"libgphoto2_port: {gp.gp_port_library_version(gp.GP_VERSION_VERBOSE)}")

        # enable logging to python. need to store callback, otherwise logging does not work.
        # gphoto2 logging is too verbose, reduce mapping
        self._logger_callback = gp.check_result(
            gp.use_python_logging(
                mapping={
                    gp.GP_LOG_ERROR: logging.INFO,
                    gp.GP_LOG_DEBUG: logging.DEBUG - 1,
                    gp.GP_LOG_VERBOSE: logging.DEBUG - 3,
                    gp.GP_LOG_DATA: logging.DEBUG - 6,
                }
            )
        )

    def start(self):
        """To start the FrameServer, you will also need to start the Picamera2 object."""

        # check for available devices
        if not available_camera_indexes():
            raise OSError("no camera detected. abort start")

        # start camera
        try:
            self._camera.init()
        except gp.GPhoto2Error as exc:
            logger.critical("camera failed to initialize. no power? no connection?")
            logger.exception(exc)
        else:
            self._camera_connected = True
            logger.debug(f"{self.__module__} started")

        if self._config.backends.LIVEPREVIEW_ENABLED:
            self._camera_preview_available = self._check_camera_preview_available()

        self._generate_images_thread.start()
        self._stats_thread.start()

        # short sleep until backend started.
        time.sleep(0.5)

        logger.debug(f"{self.__module__} started")

    def stop(self):
        """To stop the FrameServer, first stop any client threads (that might be
        blocked in wait_for_frame), then call this stop method. Don't stop the
        Picamera2 object until the FrameServer has been stopped."""

        self._generate_images_thread.stop()
        self._stats_thread.stop()

        self._generate_images_thread.join(1)
        self._stats_thread.join(1)

        self._camera.exit()

        logger.debug(f"{self.__module__} stopped")

    def wait_for_hq_image(self):
        """
        for other threads to receive a hq JPEG image
        mode switches are handled internally automatically, no separate trigger necessary
        this function blocks until frame is received
        raise TimeoutError if no frame was received
        """
        with self._hires_data.condition:
            self._hires_data.request_ready.set()

            if not self._hires_data.condition.wait(timeout=4):
                raise TimeoutError("timeout receiving frames")

        self._hires_data.request_ready.clear()
        return self._hires_data.data

    def stats(self) -> BackendStats:
        return BackendStats(
            backend_name=__name__,
            fps=int(round(self._fps, 0)),
        )

    #
    # INTERNAL FUNCTIONS
    #

    def _check_camera_preview_available(self):
        """Test on init whether preview is available for this camera."""
        preview_available = False
        try:
            self._camera.capture_preview()
        except Exception as exc:
            logger.info(
                f"gather preview failed; disabling preview in this session. consider to disable permanently! {exc}"
            )
        else:
            preview_available = True

        return preview_available

    def _wait_for_lores_image(self):
        """for other threads to receive a lores JPEG image"""
        if self._config.backends.LIVEPREVIEW_ENABLED and not self._camera_preview_available:
            raise RuntimeError(
                "Camera cannot deliver preview stream, capture preview is disabled in this session. "
                "Consider disable livestream on gphoto2 backend permanently."
            )

        if self._generate_images_thread.stopped():
            raise RuntimeError("shutdown already in progress, abort early")

        with self._lores_data.condition:
            if not self._lores_data.condition.wait(timeout=4):
                raise TimeoutError("timeout receiving frames")
            return self._lores_data.data

    def _wait_for_lores_frame(self):
        """function not existant"""
        raise NotImplementedError

    def _on_capture_mode(self):
        # nothing to do for this backend
        pass

    def _on_preview_mode(self):
        # nothing to do for this backend
        pass

    def _gp_set_config(self, name, val):
        config = self._camera.get_config(self._camera_context)
        node = config.get_child_by_name(name)
        node.set_value(val)
        self._camera.set_config(config, self._camera_context)

    def _viewfinder(self, val=0):
        try:
            self._gp_set_config("viewfinder", val)
        except gp.GPhoto2Error as exc:
            logger.warning(f"cannot set viewfinder, command ignored {exc}")

    #
    # INTERNAL IMAGE GENERATOR
    #

    def _stats_fun(self):
        # FPS = 1 / time to process loop
        last_calc_time = time.time()  # start time of the loop

        # to calc frames per second every second
        while not self._stats_thread.stopped():
            self._fps = round(
                float(self._count) / (time.time() - last_calc_time),
                1,
            )

            # reset
            self._count = 0
            last_calc_time = time.time()

            # thread wait
            time.sleep(0.2)

    def _generate_images_fun(self):
        while not self._generate_images_thread.stopped():  # repeat until stopped
            if not self._hires_data.request_ready.is_set():
                if self._config.backends.LIVEPREVIEW_ENABLED and self._camera_preview_available:
                    try:
                        capture = self._camera.capture_preview()
                    except Exception as exc:
                        logger.critical(f"error capturing frame despite general availability. {exc}")
                        # abort this loop iteration and continue sleeping...
                        continue
                    img_bytes = memoryview(capture.get_data_and_size()).tobytes()

                    with self._lores_data.condition:
                        self._lores_data.data = img_bytes
                        self._lores_data.condition.notify_all()
                else:
                    time.sleep(0.05)
            else:
                # only capture one pic and return to lores streaming afterwards
                self._hires_data.request_ready.clear()

                # disable viewfinder;
                # allows camera to autofocus fast in native mode not contrast mode
                if self._config.backends.gphoto2_disable_viewfinder_before_capture:
                    logger.info("disable viewfinder before capture")
                    self._viewfinder(0)

                self._evtbus.emit("frameserver/onCapture")

                # capture hq picture
                logger.info("taking hq picture")
                try:
                    file_path = self._camera.capture(gp.GP_CAPTURE_IMAGE)

                    logger.info(f"Camera file path: {file_path.folder}/{file_path.name}")

                except gp.GPhoto2Error as exc:
                    logger.critical(f"error capture! check logs for errors. {exc}")

                    # inform finished anyway to signal WLED turn off lights
                    self._evtbus.emit("frameserver/onCaptureFinished")

                    # try again in next loop
                    continue

                self._evtbus.emit("frameserver/onCaptureFinished")

                # read from camera
                try:
                    if self._config.backends.gphoto2_wait_event_after_capture_trigger:
                        self._camera.wait_for_event(1000)

                    camera_file = self._camera.file_get(
                        file_path.folder,
                        file_path.name,
                        gp.GP_FILE_TYPE_NORMAL,
                    )

                    file_data = camera_file.get_data_and_size()
                    img_bytes = memoryview(file_data).tobytes()
                except gp.GPhoto2Error as exc:
                    logger.critical(f"error reading camera file! check logs for errors. {exc}")

                    # try again in next loop
                    continue

                with self._hires_data.condition:
                    self._hires_data.data = img_bytes

                    self._hires_data.condition.notify_all()

            # self._count += 1
        logger.warning("_generate_images_fun exits")


def available_camera_indexes():
    """
    find available cameras, return valid indexes.
    """

    camera_list = gp.Camera.autodetect()
    if len(camera_list) == 0:
        logger.info("no camera detected")
        return []

    available_indexes = []
    for index, (name, addr) in enumerate(camera_list):
        available_indexes.append(index)
        logger.info(f"found camera - {index}:  {addr}  {name}")

    return available_indexes
