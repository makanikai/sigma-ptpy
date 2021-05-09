from sigma_ptpy import SigmaPTPy
from sigma_ptpy.enum import ApiConfigTag
from sigma_ptpy.apex import ISOSpeedConverter, Aperture3Converter, ExpComp3Converter, ShutterSpeed3Converter

camera = SigmaPTPy()

with camera.session():
    cnf = camera.config_api()

    print("ConfigApi:")
    for tag, val in cnf:
        if tag == ApiConfigTag.CameraModel:
            print(f"  Camera Model = {val}")
        elif tag == ApiConfigTag.SerialNumber:
            print(f"  Serial Number = {val}")
        elif tag == ApiConfigTag.FirmwareVersion:
            print(f"  Firmware version = {val}")
        elif tag == ApiConfigTag.CommunicationVersion:
            print(f"  Communication Version = {val[0]}")

    d1 = camera.get_cam_data_group1()

    print("CamDataGroup1:")

    if d1.FieldPresent.ShutterSpeed:
        ss = ShutterSpeed3Converter.decode_uint8(d1.ShutterSpeed)
        print(f"  ShutterSpeed = {ss} (%#02x)" % d1.ShutterSpeed)
    if d1.FieldPresent.Aperture:
        ec = Aperture3Converter.decode_uint8(d1.Aperture)
        print(f"  Aperture = {ec} (%#02x)" % d1.Aperture)
    if d1.FieldPresent.ISOAuto:
        print(f"  ISOAuto = {str(d1.ISOAuto)}")
    if d1.FieldPresent.ISOSpeed:
        iso = ISOSpeedConverter.decode_uint8(d1.ISOSpeed)
        print(f"  ISOSpeed = {iso} (%#02x)" % d1.ISOSpeed)
    if d1.FieldPresent.ExpComp:
        ec = ExpComp3Converter.decode_uint8(d1.ExpComp)
        print(f"  ExpCompensation = {ec} (%#02x)" % d1.ExpComp)
    if d1.FieldPresent.ABValue:
        ab = ExpComp3Converter.decode_uint8(d1.ExpComp)
        print(f"  ABValue = {ab} (%#02x)" % d1.ABValue)
    if d1.FieldPresent.ABSetting:
        print(f"  ABSetting = {str(d1.ABSetting)}")
    if d1.FieldPresent.FrameBufferState:
        print(f"  FrameBufferState = {d1.FrameBufferState} (shots)")
    if d1.FieldPresent.MediaFreeSpace:
        print(f"  MediaFreeSpace = {d1.MediaFreeSpace} (shots)")
    if d1.FieldPresent.MediaStatus:
        print(f"  MediaStatus = {str(d1.MediaStatus)}")
    if d1.FieldPresent.CurrentLensFocalLength:
        print(f"  CurrentLensFocalLength = {d1.CurrentLensFocalLength} (mm)")
    if d1.FieldPresent.BatteryState:
        print(f"  BatteryState = {str(d1.BatteryState)}")
    if d1.FieldPresent.ABShotRemainNumber:
        print(f"  ABShotRemainNumber = {str(d1.ABShotRemainNumber)}")
    if d1.FieldPresent.ExpCompExcludeAB:
        print(f"  ExpCompExcludeAB = {str(d1.ExpCompExcludeAB)}")

    print("CamDataGroup2:")
    d2 = camera.get_cam_data_group2()

    if d2.FieldPresent.DriveMode:
        print(f"  DriveMode = {str(d2.DriveMode)}")
    if d2.FieldPresent.SpecialMode:
        print(f"  SpecialMode = {str(d2.SpecialMode)}")
    if d2.FieldPresent.ExposureMode:
        print(f"  ExposureMode = {str(d2.ExposureMode)}")
    if d2.FieldPresent.AEMeteringMode:
        print(f"  AEMeteringMode = {str(d2.AEMeteringMode)}")
    if d2.FieldPresent.FlashType:
        print(f"  FlashType = {str(d2.FlashType)}")
    if d2.FieldPresent.FlashMode:
        print(f"  FlashMode = {str(d2.FlashMode)}")
    if d2.FieldPresent.FlashSetting:
        print(f"  FlashSetting = {str(d2.FlashSetting)}")
    if d2.FieldPresent.WhiteBalance:
        print(f"  WhiteBalance = {str(d2.WhiteBalance)}")
    if d2.FieldPresent.Resolution:
        print(f"  Resolution = {str(d2.Resolution)}")
    if d2.FieldPresent.ImageQuality:
        print(f"  ImageQuality = {str(d2.ImageQuality)}")

    print("CamDataGroup3:")
    d3 = camera.get_cam_data_group3()

    if d3.FieldPresent.ColorSpace:
        print(f"  ColorSpace = {str(d3.ColorSpace)}")
    if d3.FieldPresent.ColorMode:
        print(f"  ColorMode = {str(d3.ColorMode)}")
    if d3.FieldPresent.LensWideFocalLength:
        print(f"  LensWideFocalLength = {str(d3.LensWideFocalLength)}")
    if d3.FieldPresent.LensTeleFocalLength:
        print(f"  LensTeleFocalLength = {str(d3.LensTeleFocalLength)}")
    if d3.FieldPresent.AFAuxLight:
        print(f"  AFAuxLight = {str(d3.AFAuxLight)}")
    if d3.FieldPresent.AFBeep:
        print(f"  AFBeep = {str(d3.AFBeep)}")
    if d3.FieldPresent.TimerSound:
        print(f"  TimerSound = {str(d3.TimerSound)}")
    if d3.FieldPresent.DestToSave:
        print(f"  DestToSave = {str(d3.DestToSave)}")

    print("CamDataGroup4:")
    d4 = camera.get_cam_data_group4()

    if d4.FieldPresent.DCCropMode:
        print(f"  DCCropMode = {str(d4.DCCropMode)}")
    if d4.FieldPresent.LVMagnifyRatio:
        print(f"  LVMagnifyRatio = {str(d4.LVMagnifyRatio)}")
    if d4.FieldPresent.HighISOExt:
        print(f"  HighISOExt = {str(d4.HighISOExt)}")
    if d4.FieldPresent.ContShootSpeed:
        print(f"  ContShootSpeed = {str(d4.ContShootSpeed)}")
    if d4.FieldPresent.HDR:
        print(f"  HDR = {str(d4.HDR)}")
    if d4.FieldPresent.DNGQuality:
        print(f"  DNGQuality = {str(d4.DNGQuality)}")
    if d4.FieldPresent.FillLight:
        print(f"  FillLight = {str(d4.FillLight)}")
    if d4.FieldPresent.EImageStab:
        print(f"  EImageStab = {str(d4.EImageStab)}")
    if d4.FieldPresent.ShutterSound:
        print(f"  ShutterSound = {str(d4.ShutterSound)}")
    if d4.FieldPresent.LOC:
        print("  LensOpticsCompensation:")
        print(f"    Distortion = {str(d4.LOCDistortion)}")
        print(f"    Chromatic Abberation = {str(d4.LOCChromaticAbberation)}")
        print(f"    Diffraction = {str(d4.LOCDiffraction)}")
        print(f"    Vignetting = {str(d4.LOCVignetting)}")
        print(f"    Color Shading = {str(d4.LOCColorShade)}")
        print(f"    Color Shading Acquirement = {str(d4.LOCColorShadeAcq)}")

    print("CamDataGroup5:")
    d5 = camera.get_cam_data_group5()

    if d5.FieldPresent.IntervalTimer:
        print(f"  IntervalTimerSecond = {str(d5.IntervalTimerSecond)}")
        print(f"  IntervalTimerFrame = {str(d5.IntervalTimerFrame)}")
        print(f"  IntervalTimerSecondRemain = {str(d5.IntervalTimerSecondRemain)}")
        print(f"  IntervalTimerFrameRemain = {str(d5.IntervalTimerFrameRemain)}")
    if d5.FieldPresent.ColorTemp:
        print(f"  ColorTemp = {str(d5.ColorTemp)}")
    if d5.FieldPresent.AspectRatio:
        print(f"  AspectRatio = {str(d5.AspectRatio)}")
    if d5.FieldPresent.ToneEffect:
        print(f"  ToneEffect = {str(d5.ToneEffect)}")
    if d5.FieldPresent.AFAuxLightEF:
        print(f"  AFAuxLightEF = {str(d5.AFAuxLightEF)}")
