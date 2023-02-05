
# WORK IN PROGRESS

This is in dev currently. Not for production.

# Photobooth Imageserver

This small python imageserver allows to use

- picameras (with or without autofocus)
- arducams (with or without autofocus)
- DSLR cameras (via gphoto2 or digicamcontrol) and
- webcams (via opencv2 or v4l)
to be used for high quality still photos and for livestream.

The imageserver controls camera's autofocus, handles led signaling when a photo is taken and streams live video to photobooth.

The booth is made from 3d printed parts, [see the documentation over here](https://github.com/mgrl/photobooth-3d).

## :heart_eyes: Features

- camera live preview
- permanent video live view in background
- contant autofocus based on the live preview
- several camera backends supported for still/livestream
- led ring signaling photo countdown and when the photo is actually taken

## :gear: Prerequisites

- Python 3.9
- Camera supported by one of the backends
- [photobooth installed](https://photoboothproject.github.io/)
- [works probably best with 3d printed photobooth and parts listed in the BOM](https://github.com/mgrl/photobooth-3d)

## :wrench: Installation

An installer is available, helping to setup a linux or windows system.
Download the installer and start it as follows:

```text
wget https://raw.githubusercontent.com/mgrl/photobooth-imageserver/dev/install.py
python install.py
```

Browse to <http://photobooth:8000> (replace photobooth by actual hostname) and see that it is working

### Integrate Photobooth and ImageServer

Replace <http://photobooth> by the actual hostname or localhost if on same server.

```text
take_picture_cmd: curl -X POST http://photobooth:8000/cmd/capture -H 'accept: application/json' -H 'Content-Type: application/json' -d '"%s"'
take_picture_msg: Done
pre_photo_cmd: curl http://photobooth:8000/cmd/frameserver/capturemode
post_photo_cmd: curl http://photobooth:8000/cmd/frameserver/previewmode
preview_url: url("http://photobooth:8000/stream.mjpg")
background_defaults: url("http://photobooth:8000/stream.mjpg")
```

### Sync Online (for file downloads via QR Code)

```text
sudo apt-get install rclone inotify-tools
```

```text
rclone config
```

Setup the remote named "boothupload"!

```text
chmod u+x ~/imageserver/boothupload.sh
cp ~/imageserver/boothupload.service ~/.config/systemd/user/
systemctl --user enable boothupload.service
systemctl --user start boothupload
systemctl --user status boothupload
```

### Setup Wifi and Hotspot

At home prefer local wifi with endless data. If this is not available connect to a mobile hotspot for online sync.

In file /etc/wpa_supplicant/wpa_supplicant.conf set a priority for local and hotspot wifi:

```text
network={
    ssid="homewifi"
    psk="passwordOfhomewifi"
    priority=10
}
network={
   ssid="mobileexpensivewifi"
   psk="passwordOfmobileexpensivewifi"
   priority=5
}
```

## :mag: Changelog

- 2023-02-05
  - added several camera backends (working: v4l, opencv, simulated, picamera2; not yet working: gphoto2, digicamcontrol)
  - added installer
  - removed rpiws2811 and integrated WLED to be platform independent
  - keyboard reads without root permission - whole app now runs as normal user
  - pydantic config management via json and env files
- 2022-10-03
  - introduced led ring
- 2022-11-06
  - refactoring
  - rclone to sync photos online for easier download
  - store exif data to images
  - changed to exposure mode short as per default

## Contribute

Develop on Windows or Linux using VScode.
Additional requirements

- backend development
  - pip install pipreqs
- frontend development
  - nodejs 16 (nodejs 18 fails proxying the devServer)
  - yarn
  - quasar cli <https://quasar.dev/start/quasar-cli>

## Troubleshooting

Check following commands and files for error messages:

```text
# logfiles from service (last 200 lines)
journalctl --user --unit=imageserver -n 200 --no-pager
# logfiles created by photobooth
cat ~/imageserver/log/qbooth.log
# check CmaFree especially for Arducams if low:
cat /proc/meminfo
```

If service crashed, kill the python process:

```text
sudo pkill -9 python3
```

### :copyright: License

The software is licensed under the MIT license.  

### :tada: Donation

If you like my work and like to keep me motivated you can buy me a coconut water:

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](localhost)
