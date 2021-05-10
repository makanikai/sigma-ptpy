from sigma_ptpy import SigmaPTPy
from sigma_ptpy.apex import ISOSpeedConverter, Aperture3Converter, ExpComp3Converter, ShutterSpeed3Converter

from sigma_ptpy.enum import ISOAuto, WhiteBalance, ColorSpace
from sigma_ptpy.schema import CamDataGroup1, CamDataGroup2, CamDataGroup3, CamDataGroup4, CamDataGroup5

camera = SigmaPTPy()

with camera.session():
    cnf = camera.config_api()

    print("ConfigApi:")
    print(f"  Camera Model = {cnf.CameraModel}")
    print(f"  Serial Number = {cnf.SerialNumber}")
    print(f"  Firmware version = {cnf.FirmwareVersion}")
    print(f"  Communication Version = {cnf.CommunicationVersion}")

    camera.set_cam_data_group1(CamDataGroup1(ISOAuto=ISOAuto.Manual))
    camera.set_cam_data_group2(CamDataGroup2(WhiteBalance=WhiteBalance.Sunlight))
    camera.set_cam_data_group3(CamDataGroup3(ColorSpace=ColorSpace.AdobeRGB))
    camera.set_cam_data_group4(CamDataGroup4(ShutterSound=2))
    camera.set_cam_data_group5(CamDataGroup5(IntervalTimerSecond=10, IntervalTimerFrame=10))

    d1 = camera.get_cam_data_group1()

    print("CamDataGroup1:")
    if d1.ShutterSpeed is not None:
        ss = ShutterSpeed3Converter.decode_uint8(d1.ShutterSpeed)
        print(f"  ShutterSpeed = {ss} (%#02x)" % d1.ShutterSpeed)
    if d1.Aperture is not None:
        ec = Aperture3Converter.decode_uint8(d1.Aperture)
        print(f"  Aperture = {ec} (%#02x)" % d1.Aperture)
    if d1.ISOAuto is not None:
        print(f"  ISOAuto = {str(d1.ISOAuto)}")
    if d1.ISOSpeed is not None:
        iso = ISOSpeedConverter.decode_uint8(d1.ISOSpeed)
        print(f"  ISOSpeed = {iso} (%#02x)" % d1.ISOSpeed)
    if d1.ExpComp is not None:
        ec = ExpComp3Converter.decode_uint8(d1.ExpComp)
        print(f"  ExpCompensation = {ec} (%#02x)" % d1.ExpComp)
    if d1.ABValue is not None:
        ab = ExpComp3Converter.decode_uint8(d1.ExpComp)
        print(f"  ABValue = {ab} (%#02x)" % d1.ABValue)

    print(f"  ABSetting = {str(d1.ABSetting)}")
    print(f"  FrameBufferState = {d1.FrameBufferState} (shots)")
    print(f"  MediaFreeSpace = {d1.MediaFreeSpace} (shots)")
    print(f"  MediaStatus = {str(d1.MediaStatus)}")
    print(f"  CurrentLensFocalLength = {d1.CurrentLensFocalLength} (mm)")
    print(f"  BatteryState = {str(d1.BatteryState)}")
    print(f"  ABShotRemainNumber = {str(d1.ABShotRemainNumber)}")
    print(f"  ExpCompExcludeAB = {str(d1.ExpCompExcludeAB)}")

    d2 = camera.get_cam_data_group2()

    print("CamDataGroup2:")
    print(f"  DriveMode = {str(d2.DriveMode)}")
    print(f"  SpecialMode = {str(d2.SpecialMode)}")
    print(f"  ExposureMode = {str(d2.ExposureMode)}")
    print(f"  AEMeteringMode = {str(d2.AEMeteringMode)}")
    print(f"  FlashType = {str(d2.FlashType)}")
    print(f"  FlashMode = {str(d2.FlashMode)}")
    print(f"  FlashSetting = {str(d2.FlashSetting)}")
    print(f"  WhiteBalance = {str(d2.WhiteBalance)}")
    print(f"  Resolution = {str(d2.Resolution)}")
    print(f"  ImageQuality = {str(d2.ImageQuality)}")

    d3 = camera.get_cam_data_group3()

    print("CamDataGroup3:")
    print(f"  ColorSpace = {str(d3.ColorSpace)}")
    print(f"  ColorMode = {str(d3.ColorMode)}")
    print(f"  LensWideFocalLength = {str(d3.LensWideFocalLength)}")
    print(f"  LensTeleFocalLength = {str(d3.LensTeleFocalLength)}")
    print(f"  AFAuxLight = {str(d3.AFAuxLight)}")
    print(f"  AFBeep = {str(d3.AFBeep)}")
    print(f"  TimerSound = {str(d3.TimerSound)}")
    print(f"  DestToSave = {str(d3.DestToSave)}")

    d4 = camera.get_cam_data_group4()

    print("CamDataGroup4:")
    print(f"  DCCropMode = {str(d4.DCCropMode)}")
    print(f"  LVMagnifyRatio = {str(d4.LVMagnifyRatio)}")
    print(f"  HighISOExt = {str(d4.HighISOExt)}")
    print(f"  ContShootSpeed = {str(d4.ContShootSpeed)}")
    print(f"  HDR = {str(d4.HDR)}")
    print(f"  DNGQuality = {str(d4.DNGQuality)}")
    print(f"  FillLight = {str(d4.FillLight)}")
    print(f"  EImageStab = {str(d4.EImageStab)}")
    print(f"  ShutterSound = {str(d4.ShutterSound)}")
    print("  LensOpticsCompensation:")
    print(f"    Distortion = {str(d4.LOCDistortion)}")
    print(f"    Chromatic Abberation = {str(d4.LOCChromaticAbberation)}")
    print(f"    Diffraction = {str(d4.LOCDiffraction)}")
    print(f"    Vignetting = {str(d4.LOCVignetting)}")
    print(f"    Color Shading = {str(d4.LOCColorShade)}")
    print(f"    Color Shading Acquirement = {str(d4.LOCColorShadeAcq)}")

    d5 = camera.get_cam_data_group5()

    print("CamDataGroup5:")
    print(f"  IntervalTimerSecond = {str(d5.IntervalTimerSecond)}")
    print(f"  IntervalTimerFrame = {str(d5.IntervalTimerFrame)}")
    print(f"  IntervalTimerSecondRemain = {str(d5.IntervalTimerSecondRemain)}")
    print(f"  IntervalTimerFrameRemain = {str(d5.IntervalTimerFrameRemain)}")
    print(f"  ColorTemp = {str(d5.ColorTemp)}")
    print(f"  AspectRatio = {str(d5.AspectRatio)}")
    print(f"  ToneEffect = {str(d5.ToneEffect)}")
    print(f"  AFAuxLightEF = {str(d5.AFAuxLightEF)}")

    focus = camera.get_cam_data_group_focus()

    print("CamDataGroupFocus:")
    print(f"  FocusMode = {str(focus.FocusMode)}")
    print(f"  AFLock = {str(focus.AFLock)}")
    print(f"  FaceEyeAF = {str(focus.FaceEyeAF)}")
    print(f"  FaceEyeAFStatus = {str(focus.FaceEyeAFStatus)}")
    print(f"  FocusArea = {str(focus.FocusArea)}")
    print(f"  OnePointSelection = {str(focus.OnePointSelection)}")
    print(f"  Distance Measurement Frame size = {str(focus.DMFSize)}")
    print(f"  Distance Measurement Frame position = {str(focus.DMFPos)}")
    print(f"  Distance Measurement Frame detection status = {str(focus.DMFDetection)}")
    print(f"  Pre AF / Constant AF = {str(focus.PreConstAF)}")
    print(f"  Focus Limit = {str(focus.FocusLimit)}")
