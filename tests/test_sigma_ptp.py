import unittest
from sigma_ptpy import SigmaPTP
from sigma_ptpy.enum import (
    DriveMode, SpecialMode, ExposureMode, AEMeteringMode, FlashType, FlashMode, FlashSetting,
    WhiteBalance, Resolution, ImageQuality, ColorSpace, ColorMode,
    BatteryKind, AFAuxLight, CaptureMode, CaptStatus, DestToSave
)

class TestSigmaPTP(unittest.TestCase):
    def test_CamDataGroup1_ShutterSpeed(self):
        fmt = SigmaPTP()._CamDataGroup1
        res = fmt.parse(b"\x03\x01\x00\x10\x14")
        self.assertEqual(res.FieldPresent.ShutterSpeed, 1)
        self.assertEqual(res.ShutterSpeed, 16) # SS=30s

        res = fmt.parse(b"\x03\x01\x00\x5B\x5F")
        self.assertEqual(res.FieldPresent.ShutterSpeed, 1)
        self.assertEqual(res.ShutterSpeed, 91) # SS=1/20s

    def test_CamDataGroup1_Aperture(self):
        fmt = SigmaPTP()._CamDataGroup1
        res = fmt.parse(b"\x03\x02\x00\x20\x25")
        self.assertEqual(res.FieldPresent.Aperture, 1)
        self.assertEqual(res.Aperture, 32) # F=2.8

        res = fmt.parse(b"\x03\x02\x00\x28\x2D")
        self.assertEqual(res.FieldPresent.Aperture, 1)
        self.assertEqual(res.Aperture, 40) # F=4.0

    def test_CamDataGroup1_ISOAuto(self):
        fmt = SigmaPTP()._CamDataGroup1
        res = fmt.parse(b"\x03\x08\x00\x00\x0B")
        self.assertEqual(res.FieldPresent.ISOAuto, 1)
        self.assertEqual(res.ISOAuto, 0)

        res = fmt.parse(b"\x03\x08\x00\x01\x0C")
        self.assertEqual(res.FieldPresent.ISOAuto, 1)
        self.assertEqual(res.ISOAuto, 1)

    def test_CamDataGroup1_ISOSpeed(self):
        fmt = SigmaPTP()._CamDataGroup1
        res = fmt.parse(b"\x03\x10\x00\x20\x33")
        self.assertEqual(res.FieldPresent.ISOSpeed, 1)
        self.assertEqual(res.ISOSpeed, 32) # ISO=100

        res = fmt.parse(b"\x03\x10\x00\x48\x5B")
        self.assertEqual(res.FieldPresent.ISOSpeed, 1)
        self.assertEqual(res.ISOSpeed, 72) # ISO=3200

    def test_CamDataGroup1_RecvData(self):
        fmt = SigmaPTP()._CamDataGroup1
        res = fmt.parse(b"\x13\xff\x7f\x20\x20\x00\x01\xf8\x00\x00\x01\tk\x03\x01\xd0\x02\x08\x00\x00\x1d")

        self.assertEqual(res.FieldPresent.ShutterSpeed, 1)
        self.assertEqual(res.ShutterSpeed, 0x20)
        self.assertEqual(res.FieldPresent.Aperture, 1)
        self.assertEqual(res.Aperture, 0x20)
        self.assertEqual(res.FieldPresent.ProgramShift, 1)
        self.assertEqual(res.ProgramShift, 0x00)
        self.assertEqual(res.FieldPresent.ISOAuto, 1)
        self.assertEqual(res.ISOAuto, 1)
        self.assertEqual(res.FieldPresent.ISOSpeed, 1)
        self.assertEqual(res.ISOSpeed, 0xf8)
        self.assertEqual(res.FieldPresent.ExpCompensation, 1)
        self.assertEqual(res.ExpCompensation, 0)
        self.assertEqual(res.FieldPresent.ABValue, 1)
        self.assertEqual(res.ABValue, 0)
        self.assertEqual(res.FieldPresent.ABSetting, 1)
        self.assertEqual(res.ABSetting, 1)

        self.assertEqual(res.FieldPresent.FrameBufferState, 1)
        self.assertEqual(res.FrameBufferState, 0x09)
        self.assertEqual(res.FieldPresent.MediaFreeSpace, 1)
        self.assertEqual(res.MediaFreeSpace, 0x036B)
        self.assertEqual(res.FieldPresent.MediaStatus, 1)
        self.assertEqual(res.MediaStatus, 0x01)
        self.assertEqual(res.FieldPresent.CurrentLensFocalLength, 1)
        self.assertEqual(res.CurrentLensFocalLength, 0x02d0)
        self.assertEqual(res.FieldPresent.BatteryState, 1)
        self.assertEqual(res.BatteryState, 0x08)
        self.assertEqual(res.FieldPresent.ABShotRemainNumber, 1)
        self.assertEqual(res.ABShotRemainNumber, 0)
        self.assertEqual(res.FieldPresent.ExpCompExcludeAB, 1)
        self.assertEqual(res.ExpCompExcludeAB, 0)

    def test_CamDataGroup2_ExposureMode(self):
        fmt = SigmaPTP()._CamDataGroup2
        res = fmt.parse(b"\x03\x04\x00\x04\x0B")
        self.assertEqual(res.FieldPresent.ExposureMode, 1)
        self.assertEqual(res.ExposureMode, ExposureMode.Manual)

    def test_CamDataGroup2_WhiteBalance(self):
        fmt = SigmaPTP()._CamDataGroup2
        res = fmt.parse(b"\x03\x00\x20\x01\x24")
        self.assertEqual(res.FieldPresent.WhiteBalance, 1)
        self.assertEqual(res.WhiteBalance, WhiteBalance.Auto)

        res = fmt.parse(b"\x03\x00\x20\x06\x29")
        self.assertEqual(res.FieldPresent.WhiteBalance, 1)
        self.assertEqual(res.WhiteBalance, WhiteBalance.Fluorescent)

    def test_CamDataGroup2_RecvData(self):
        fmt = SigmaPTP()._CamDataGroup2
        res = fmt.parse(b"\x0e\x3f\xfc\x07\x02\x04\x01\x00\x03\x00\x00\x00\x01\x01\x10l")

        self.assertEqual(res.FieldPresent.DriveMode, 1)
        self.assertEqual(res.DriveMode, DriveMode.IntervalTimer)
        self.assertEqual(res.FieldPresent.SpecialMode, 1)
        self.assertEqual(res.SpecialMode, SpecialMode.LiveView)
        self.assertEqual(res.FieldPresent.ExposureMode, 1)
        self.assertEqual(res.ExposureMode, ExposureMode.Manual)
        self.assertEqual(res.FieldPresent.AEMeteringMode, 1)
        self.assertEqual(res.AEMeteringMode, AEMeteringMode.Evaluative)
        self.assertEqual(res.FieldPresent.FlashType, 0)
        self.assertEqual(res.FieldPresent.FlashMode, 1)
        self.assertEqual(res.FlashMode, FlashMode.Normal)
        self.assertEqual(res.FieldPresent.FlashSetting, 1)
        self.assertEqual(res.FlashSetting, FlashSetting.Null)
        self.assertEqual(res.FieldPresent.WhiteBalance, 1)
        self.assertEqual(res.WhiteBalance, WhiteBalance.Auto)
        self.assertEqual(res.FieldPresent.Resolution, 1)
        self.assertEqual(res.Resolution, Resolution.High)
        self.assertEqual(res.FieldPresent.ImageQuality, 1)
        self.assertEqual(res.ImageQuality, ImageQuality.DNG)


    def test_CamDataGroup3_RecvData(self):
        fmt = SigmaPTP()._CamDataGroup3
        res = fmt.parse(b"\x10\xff\xa3\x00\x00\x00\x01\x03\x02\x00\xd0\x00\x00\x02\x05\x05\x02\x96")

        self.assertEqual(res.FieldPresent.ColorSpace, 1)
        self.assertEqual(res.ColorSpace, ColorSpace.sRGB)
        self.assertEqual(res.FieldPresent.ColorMode, 1)
        self.assertEqual(res.ColorMode, ColorMode.Standard)
        self.assertEqual(res.FieldPresent.BatteryKind, 1)
        self.assertEqual(res.BatteryKind, BatteryKind.ACAdapter)
        self.assertEqual(res.FieldPresent.LensWideFocalLength, 1)
        self.assertEqual(res.LensWideFocalLength, 0xd000)
        self.assertEqual(res.FieldPresent.LensTeleFocalLength, 1)
        self.assertEqual(res.LensTeleFocalLength, 0x0000)
        self.assertEqual(res.FieldPresent.AFAuxLight, 1)
        self.assertEqual(res.AFAuxLight, AFAuxLight.OFF)
        self.assertEqual(res.FieldPresent.AFBeep, 1)
        self.assertEqual(res.AFBeep, 0x05)
        self.assertEqual(res.FieldPresent.TimerSound, 1)
        self.assertEqual(res.TimerSound, 0x05)
        self.assertEqual(res.FieldPresent.DestToSave, 1)
        self.assertEqual(res.DestToSave, DestToSave.InComputer)

    def test_CamCaptStatus_RecvData(self):
        fmt = SigmaPTP()._CamCaptStatus

        res = fmt.parse(b"\x06\x00\x00\x01\x01\x00\x03\x0B")
        self.assertEqual(res.ImageId, 0)
        self.assertEqual(res.ImageDBHead, 0)
        self.assertEqual(res.ImageDBTail, 1)
        self.assertEqual(res.CaptStatus, CaptStatus.ShootInProgress)
        self.assertEqual(res.DestToSave, DestToSave.Both)

        res = fmt.parse(b"\x06\x00\x00\x01\x04\x00\x03\x0E")
        self.assertEqual(res.ImageId, 0)
        self.assertEqual(res.ImageDBHead, 0)
        self.assertEqual(res.ImageDBTail, 1)
        self.assertEqual(res.CaptStatus, CaptStatus.ImageGenInProgress)
        self.assertEqual(res.DestToSave, DestToSave.Both)

    def test_PictFileInfo2_RecvData(self):
        fmt = SigmaPTP()._PictFileInfo2

        res = fmt.parse(b"\x38\x00\x00\x00\x01\x00\x00\x00\x0C\x00\x00\x00\x80\x05\x00\x57\x42\x3E\x0A\x00\x24\x00\x00\x00\x2D\x00\x00\x00\x4A\x50\x47\x00\x70\x17\xA0\x0F\x31\x30\x30\x53\x49\x47\x4D\x41\x00\x53\x44\x49\x4D\x30\x30\x30\x31\x2E\x4A\x50\x47\x00\x03\x00")
        self.assertEqual(res.FileAddress, 0x57000580)
        self.assertEqual(res.FileSize, 0x000a3e42)
        self.assertEqual(res.PictureFormat, b"JPG")
        self.assertEqual(res.SizeX, 6000)
        self.assertEqual(res.SizeY, 4000)
        self.assertEqual(res.PathName, b"100SIGMA")
        self.assertEqual(res.FileName, b"SDIM0001.JPG")


if __name__ == '__main__':
    unittest.main()
