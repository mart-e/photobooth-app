import os
import json
import logging
logger = logging.getLogger(__name__)

CONFIG_FILENAME = "config.json"


class CONFIG():

    def __init__(self):
        # quality
        self.CAPTURE_CAM_RESOLUTION = (4656, 3496)
        self.CAPTURE_VIDEO_RESOLUTION = (1280, 720)
        self.PREVIEW_CAM_RESOLUTION = (2328, 1748)
        self.PREVIEW_VIDEO_RESOLUTION = (1280, 720)
        self.LORES_QUALITY = 80
        self.HIRES_QUALITY = 90

        # capture
        # Normal/Short(/Long/Custom)
        self.CAPTURE_EXPOSURE_MODE = "short"
        self.CAMERA_TUNINGFILE = "imx519.json"

        # autofocus
        # 70 for imx519 (range 0...4000) and 30 for arducam64mp (range 0...1000)
        self.FOCUSER_MIN_VALUE = 300
        self.FOCUSER_MAX_VALUE = 3000
        self.FOCUSER_DEF_VALUE = 800
        self.FOCUSER_STEP = 50
        self.FOCUSER_MOVE_TIME = 0.066
        self.FOCUSER_JPEG_QUALITY = 85
        self.FOCUSER_ROI = (0.2, 0.2, 0.6, 0.6)  # x, y, width, height
        self.FOCUSER_DEVICE = "/dev/v4l-subdev1"
        self.FOCUSER_REPEAT_TRIGGER = 5  # every x seconds trigger autofocus

        # dont change following defaults. If necessary change via argument
        self.DEBUG = False
        self.DEBUG_OVERLAY = False
        self.DEBUG_SHOWPREVIEW = False

        # infoled / ws2812b ring settings
        self.WS2812_NUMBER_LEDS = 12
        self.WS2812_GPIO_PIN = 18
        self.WS2812_COLOR = (255, 255, 255, 255)    # RGBW
        self.WS2812_CAPTURE_COLOR = (0, 125, 125, 0)  # RGBW
        self.WS2812_MAX_BRIGHTNESS = 50
        self.WS2812_ANIMATION_UPDATE = 70    # update circle animation every XX ms

        # location service
        self.LOCATION_SERVICE_ENABLED = True
        self.LOCATION_SERVICE_API_KEY = ""
        self.LOCATION_SERVICE_CONSIDER_IP = True
        self.LOCATION_SERVICE_WIFI_INTERFACE_NO = 0
        self.LOCATION_SERVICE_FORCED_UPDATE = 60  # every x minutes
        # retries after program start to get more accurate data
        self.LOCATION_SERVICE_HIGH_FREQ_UPDATE = 10
        # threshold below which the data is accurate enough to not trigger high freq updates (in meter)
        self.LOCATION_SERVICE_THRESHOLD_ACCURATE = 1000

        self.LOGGING_CONFIG = {
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s %(funcName)s() L%(lineno)-4d %(message)s'
                },
                'detailed': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s %(funcName)s() L%(lineno)-4d %(message)s call_trace=%(pathname)s L%(lineno)-4d'

                },
            },
            'handlers': {
                'default': {
                    'level': 'DEBUG',
                    'formatter': 'standard',
                    'class': 'logging.StreamHandler',
                    # 'stream': 'ext://sys.stdout',  # Default is stderr
                },
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'detailed',
                    'filename': 'photobooth.log',
                    'maxBytes': 102400,
                    'backupCount': 3,
                },
                'eventstream': {
                    'class': '__main__.EventstreamLogHandler',
                    'formatter': 'standard',
                }
            },
            'loggers': {
                '': {  # root logger
                    'handlers': ['default', 'eventstream'],
                    'level': 'DEBUG',
                    'propagate': False
                },
                '__main__': {  # if __name__ == '__main__'
                    'handlers': ['default', 'eventstream'],
                    'level': 'DEBUG',
                    'propagate': False
                },
                'picamera2': {
                    'handlers': ['default'],
                    'level': 'INFO',
                    'propagate': False
                },
                'pywifi': {
                    'handlers': ['default'],
                    'level': 'WARNING',
                    'propagate': False
                },
                'sse_starlette.sse': {
                    'handlers': ['default'],
                    'level': 'INFO',
                    'propagate': False
                },
                'lib.Autofocus': {
                    'handlers': ['default'],
                    'level': 'INFO',
                    'propagate': False
                },
            }
        }

    def reset_default_values(self):
        self.__dict__ = vars(CONFIG())

        try:
            os.remove(CONFIG_FILENAME)
        except:
            logger.info("delete settings.json file failed.")

        # self._publishSSE_currentconfig()

    def load(self):
        try:
            with open(CONFIG_FILENAME, "r") as read_file:
                read_settings = json.load(read_file)

                for key in self.__dict__:
                    # check whether a setting is avail from file and update default
                    if key in read_settings:
                        self.__dict__[key] = read_settings[key]

            logger.debug(f"loaded following config: {self.__dict__}")
            # self._publishSSE_currentconfig()

        except Exception as e:
            logger.info(f"load settings failed (no file?) {e}")

    def save(self):
        # save only non-default values:
        ##set_defaults = set(vars(CONFIG()).items())
        # print(set_defaults)
        ##set_current = set(self.__dict__.items())
        # print(set_current)
        ##save_dict = dict(set_current-set_defaults)
        save_dict = self.__dict__
        logger.debug(f"saving following dict: {save_dict}")
        with open(CONFIG_FILENAME, "w") as write_file:
            json.dump(save_dict, write_file, indent=4)

        # self._publishSSE_currentconfig()

    def _publishSSEInitial(self):   # TODO, refactor class to make this possible
        self._publishSSE_currentconfig()

    def _publishSSE_currentconfig(self):
        self._ee.emit("publishSSE", sse_event="config/currentconfig",
                      sse_data=json.dumps(self.__dict__))
