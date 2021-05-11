# sigma-ptpy [![Python package](https://github.com/akabe/sigma-ptpy/actions/workflows/test.yaml/badge.svg)](https://github.com/akabe/sigma-ptpy/actions/workflows/test.yaml)

A third-party camera control library for the [SIGMA fp series](https://www.sigma-global.com/en/cameras/fp/).

The SIGMA fp series is a set of full-size mirrorless cameras developed by [SIGMA Corp](https://www.sigma-global.com/en/).
The cameras supports PTP (Picture Transfer Protocol; ISO15740) for access to functionality of them
from computers such as

- getting and setting parameters (shutter speed, aperture, white balance, color mode, etc.),
- taking pictures,
- live view,

and so on. This Python library provides a part of the opration on the fp series.

API doc is built by Sphinx, and is available on [online](https://akabe.github.io/sigma-ptpy/index.html).

## Getting started

The latest version can be installed by

```sh
pip install git+https://github.com/akabe/sigma-ptpy.git
```

After the installation, connect your SIGMA fp to your computer with "Camera Control" mode and
type the following command. If the camera is detected, a message is printed.

```console
$ python examples/get_info.py
CamDataGroup1:
  ShutterSpeed = None (0x0)
  Aperture = None (0x0)
  ISOAuto = ISOAuto.Auto
  ISOSpeed = None (0xf8)
  ExpCompensation = 0.0 (0x0)
  ABValue = 0.0 (0x0)
  ABSetting = ABSetting.AB3ZeroMinusPlus
  FrameBufferState = 9 (shots)
  MediaFreeSpace = 2901 (shots)
  MediaStatus = 1
  CurrentLensFocalLength = 45.0 (mm)
  BatteryState = 8
  ABShotRemainNumber = 0
  ExpCompExcludeAB = 0
CamDataGroup2:
  DriveMode = DriveMode.SingleCapture
  SpecialMode = SpecialMode.LiveView
  ExposureMode = ExposureMode.ProgramAuto
  AEMeteringMode = AEMeteringMode.Null
  FlashMode = FlashMode.Normal
  FlashSetting = FlashSetting.Null
  WhiteBalance = WhiteBalance.Auto
  Resolution = Resolution.High
  ImageQuality = ImageQuality.JPEGFine
CamDataGroup3:
  ColorSpace = ColorSpace.sRGB
  ColorMode = ColorMode.Standard
  LensWideFocalLength = 3840.0
  LensTeleFocalLength = 3840.0
  AFAuxLight = AFAuxLight.OFF
  AFBeep = 5
  TimerSound = 5
  DestToSave = DestToSave.Null
```

## Related work

SIGMA Corp distributes the [SIGMA Camera Control SDK](https://www.sigma-global.com/en/news/2020/07/02/10916/) for the SIGMA fp series. The official library fully supports the functionality of the cameras, and includes API documents, C/Objective-C headers, and compiled binary files for Windows and Mac.

[libgphoto2](http://www.gphoto.org/) is a open-source framework designed to allow access to digital cameras by external programs. It provides operations on a lot of cameras such as Canon, Nikon, and Sony, but SIGMA fp is less supported at the current version v2.5.27.

## Contribution

Fork and create a PR, please.
Don't forget run `python setup.py test` and `./git/pre-commit` before a PR.
