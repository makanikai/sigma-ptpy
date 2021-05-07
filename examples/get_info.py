from sigma_ptpy import SigmaPTPy
from sigma_ptpy.apex import ISOSpeedConverter, Aperture3Converter, ExpComp3Converter, ShutterSpeed3Converter

camera = SigmaPTPy()

with camera.session():
    camera.config_api()

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
