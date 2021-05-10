import unittest
from sigma_ptpy.enum import (
    DirectoryType,
    DriveMode, SpecialMode, ExposureMode, AEMeteringMode, FlashMode, FlashSetting,
    WhiteBalance, Resolution, ImageQuality, ColorSpace, ColorMode,
    BatteryKind, AFAuxLight, CaptStatus, DestToSave,
    DCCropMode, LVMagnifyRatio, HighISOExt, ContShootSpeed, HDR,
    DNGQuality, LOCDistortion, LOCChromaticAbberation, LOCDiffraction,
    LOCVignetting, LOCColorShade, LOCColorShadeAcq, EImageStab,
    ToneEffect, AspectRatio)
from sigma_ptpy.schema import (
    CamDataGroup1, CamDataGroup2, CamDataGroup3, CamDataGroup4, CamDataGroup5,
    CamCaptStatus, PictFileInfo2, _DirectoryEntrySchema)


class Test_DirectoryEntrySchema(unittest.TestCase):
    this = _DirectoryEntrySchema()

    def test_decode_UInt8(self):
        actual = self.this._decode(
            b"\x14\x00\x00\x00"
            b"\x01\x00\x00\x00"
            b"\x01\x00\x01\x00\x01\x00\x00\x00\x9c\x00\x00\x00")
        expected = [(1, [0x9c])]
        self.assertEqual(actual, expected)

        actual = self.this._decode(
            b"\x1c\x00\x00\x00"
            b"\x01\x00\x00\x00"
            b"\x01\x00\x01\x00\x05\x00\x00\x00\x14\x00\x00\x00"
            b"\x1c\x2c\x3c\x4c\x5c\x00\x00\x00")
        expected = [(1, [0x1c, 0x2c, 0x3c, 0x4c, 0x5c])]
        self.assertEqual(actual, expected)

    def test_decode_String(self):
        actual = self.this._decode(
            b"\x14\x00\x00\x00"
            b"\x01\x00\x00\x00"
            b"\x01\x00\x02\x00\x04\x00\x00\x00V82\x00")
        expected = [(1, "V82")]
        self.assertEqual(actual, expected)

        actual = self.this._decode(
            b"\x20\x00\x00\x00"
            b"\x01\x00\x00\x00"
            b"\x01\x00\x02\x00\x09\x00\x00\x00\x14\x00\x00\x00"
            b"SIGMA fp\x00\x00\x00\x00")
        expected = [(1, "SIGMA fp")]
        self.assertEqual(actual, expected)

    def test_decode_RecvData(self):
        rawdata = \
            b"\x4a\x00\x00\x00\x04\x00\x00\x00\x01\x00\x02\x00\x09\x00\x00\x00\x3c\x00\x00\x00\x02" \
            b"\x00\x02\x00\x09\x00\x00\x00\x45\x00\x00\x00\x03\x00\x02\x00\x04\x00\x00\x00\x56\x38" \
            b"\x32\x00\x05\x00\x0b\x00\x01\x00\x00\x00\x52\xb8\x9e\x3f\x00\x00\x00\x00\x53\x49\x47" \
            b"\x4d\x41\x20\x66\x70\x00\x39\x31\x34\x30\x32\x30\x38\x31\x00\xa9"
        actual = self.this._decode(rawdata)

        self.assertEqual(len(actual), 4)
        self.assertEqual(actual[0], (1, "SIGMA fp"))
        self.assertEqual(actual[1], (2, "91402081"))
        self.assertEqual(actual[2], (3, "V82"))
        self.assertEqual(actual[3][0], 5)
        self.assertAlmostEqual(actual[3][1][0], 1.2400000095367432)

    def test_encode_UInt8(self):
        arg = [
            (1, DirectoryType.UInt8, 0x9c)
        ]
        actual = self.this._encode(arg)
        expected = \
            b"\x14\x00\x00\x00" \
            b"\x01\x00\x00\x00" \
            b"\x01\x00\x01\x00\x01\x00\x00\x00\x9c\x00\x00\x00"
        self.assertEqual(actual, expected)

        arg = [
            (1, DirectoryType.UInt8, [0x1c, 0x2c, 0x3c, 0x4c, 0x5c])
        ]
        actual = self.this._encode(arg)
        expected = \
            b"\x1c\x00\x00\x00" \
            b"\x01\x00\x00\x00" \
            b"\x01\x00\x01\x00\x05\x00\x00\x00\x14\x00\x00\x00" \
            b"\x1c\x2c\x3c\x4c\x5c\x00\x00\x00"
        self.assertEqual(actual, expected)

    def test_encode_String(self):
        arg = [(1, DirectoryType.String, "V82")]
        actual = self.this._encode(arg)
        expected = \
            b"\x14\x00\x00\x00" \
            b"\x01\x00\x00\x00" \
            b"\x01\x00\x02\x00\x04\x00\x00\x00V82\x00"
        self.assertEqual(actual, expected)

        arg = [(1, DirectoryType.String, "SIGMA fp")]
        actual = self.this._encode(arg)
        expected = \
            b"\x20\x00\x00\x00" \
            b"\x01\x00\x00\x00" \
            b"\x01\x00\x02\x00\x09\x00\x00\x00\x14\x00\x00\x00" \
            b"SIGMA fp\x00\x00\x00\x00"
        self.assertEqual(actual, expected)


class Test_CamDataGroup1(unittest.TestCase):
    def test_ShutterSpeed(self):
        res = CamDataGroup1()
        res.decode(b"\x03\x01\x00\x10\x14")
        self.assertEqual(res.ShutterSpeed, 16)  # SS=30s

        res = CamDataGroup1()
        res.decode(b"\x03\x01\x00\x5B\x5F")
        self.assertEqual(res.ShutterSpeed, 91)  # SS=1/20s

    def test_Aperture(self):
        res = CamDataGroup1()
        res.decode(b"\x03\x02\x00\x20\x25")
        self.assertEqual(res.Aperture, 32)  # F=2.8

        res = CamDataGroup1()
        res.decode(b"\x03\x02\x00\x28\x2D")
        self.assertEqual(res.Aperture, 40)  # F=4.0

    def test_ISOAuto(self):
        res = CamDataGroup1()
        res.decode(b"\x03\x08\x00\x00\x0B")
        self.assertEqual(res.ISOAuto, 0)

        res = CamDataGroup1()
        res.decode(b"\x03\x08\x00\x01\x0C")
        self.assertEqual(res.ISOAuto, 1)

    def test_ISOSpeed(self):
        res = CamDataGroup1()
        res.decode(b"\x03\x10\x00\x20\x33")
        self.assertEqual(res.ISOSpeed, 32)  # ISO=100

        res = CamDataGroup1()
        res.decode(b"\x03\x10\x00\x48\x5B")
        self.assertEqual(res.ISOSpeed, 72)  # ISO=3200

    def test_RecvData(self):
        res = CamDataGroup1()
        res.decode(b"\x13\xff\x7f\x20\x20\x00\x01\xf8\x00\x00\x01\tk\x03\x01\xd0\x02\x08\x00\x00\x1d")

        self.assertEqual(res.ShutterSpeed, 0x20)
        self.assertEqual(res.Aperture, 0x20)
        self.assertEqual(res.ProgramShift, 0x00)
        self.assertEqual(res.ISOAuto, 1)
        self.assertEqual(res.ISOSpeed, 0xf8)
        self.assertEqual(res.ExpComp, 0)
        self.assertEqual(res.ABValue, 0)
        self.assertEqual(res.ABSetting, 1)

        self.assertEqual(res.FrameBufferState, 0x09)
        self.assertEqual(res.MediaFreeSpace, 0x036B)
        self.assertEqual(res.MediaStatus, 0x01)
        self.assertEqual(res.CurrentLensFocalLength, 45.0)
        self.assertEqual(res.BatteryState, 0x08)
        self.assertEqual(res.ABShotRemainNumber, 0)
        self.assertEqual(res.ExpCompExcludeAB, 0)


class Test_CamDataGroup2(unittest.TestCase):
    def test_ExposureMode(self):
        res = CamDataGroup2()
        res.decode(b"\x03\x04\x00\x04\x0B")
        self.assertEqual(res.ExposureMode, ExposureMode.Manual)

    def test_WhiteBalance(self):
        res = CamDataGroup2()
        res.decode(b"\x03\x00\x20\x01\x24")
        self.assertEqual(res.WhiteBalance, WhiteBalance.Auto)

        res = CamDataGroup2()
        res.decode(b"\x03\x00\x20\x06\x29")
        self.assertEqual(res.WhiteBalance, WhiteBalance.Fluorescent)

    def test_RecvData(self):
        res = CamDataGroup2()
        res.decode(b"\x0e\x3f\xfc\x07\x02\x04\x01\x00\x03\x00\x00\x00\x01\x01\x10l")

        self.assertEqual(res.DriveMode, DriveMode.IntervalTimer)
        self.assertEqual(res.SpecialMode, SpecialMode.LiveView)
        self.assertEqual(res.ExposureMode, ExposureMode.Manual)
        self.assertEqual(res.AEMeteringMode, AEMeteringMode.Evaluative)
        self.assertEqual(res.FlashMode, FlashMode.Normal)
        self.assertEqual(res.FlashSetting, FlashSetting.Null)
        self.assertEqual(res.WhiteBalance, WhiteBalance.Auto)
        self.assertEqual(res.Resolution, Resolution.High)
        self.assertEqual(res.ImageQuality, ImageQuality.DNG)


class Test_CamDataGroup3(unittest.TestCase):
    def test_RecvData(self):
        res = CamDataGroup3()
        res.decode(b"\x10\xff\xa3\x00\x00\x00\x01\x03\x02\x00\xd0\x00\x00\x02\x05\x05\x02\x96")

        self.assertEqual(res.ColorSpace, ColorSpace.sRGB)
        self.assertEqual(res.ColorMode, ColorMode.Standard)
        self.assertEqual(res.BatteryKind, BatteryKind.ACAdapter)
        self.assertEqual(res.LensWideFocalLength, 0xd00 + 0.0)
        self.assertEqual(res.LensTeleFocalLength, 0x0000)
        self.assertEqual(res.AFAuxLight, AFAuxLight.Off)
        self.assertEqual(res.AFBeep, 0x05)
        self.assertEqual(res.TimerSound, 0x05)
        self.assertEqual(res.DestToSave, DestToSave.InComputer)


class Test_CamDataGroup4(unittest.TestCase):
    def test_RecvData(self):
        res = CamDataGroup4()
        res.decode(b"\x11\xf0\x3f\x00\x03\x01\x03\xff\x0e\x00\x01\x01\x02\x01\xfe\x02\x02\x05\x60")

        self.assertEqual(res.DCCropMode, DCCropMode.Auto)
        self.assertEqual(res.LVMagnifyRatio, LVMagnifyRatio.x8)
        self.assertEqual(res.HighISOExt, HighISOExt.Off)
        self.assertEqual(res.ContShootSpeed, ContShootSpeed.Low)
        self.assertEqual(res.HDR, HDR.Off)
        self.assertEqual(res.DNGQuality, DNGQuality.Q14bit)
        self.assertEqual(res.FillLight, 0x00)
        self.assertEqual(res.LOCDistortion, LOCDistortion.Auto)
        self.assertEqual(res.LOCChromaticAbberation, LOCChromaticAbberation.Auto)
        self.assertEqual(res.LOCDiffraction, LOCDiffraction.Off)
        self.assertEqual(res.LOCVignetting, LOCVignetting.Auto)
        self.assertEqual(res.LOCColorShade, LOCColorShade.Off)
        self.assertEqual(res.LOCColorShadeAcq, LOCColorShadeAcq.Off)
        self.assertEqual(res.EImageStab, EImageStab.Off)
        self.assertEqual(res.ShutterSound, 5)


class Test_CamDataGroup5(unittest.TestCase):
    def test_RecvData(self):
        res = CamDataGroup5()
        res.decode(b"\x0c\x2b\x00\x0a\x00\x01\x00\x00\x01\x58\x1b\x03\x01\xba")

        self.assertEqual(res.IntervalTimerSecond, 10)
        self.assertEqual(res.IntervalTimerFrame, 1)
        self.assertEqual(res.IntervalTimerSecondRemain, 0)
        self.assertEqual(res.IntervalTimerFrameRemain, 1)
        self.assertEqual(res.ColorTemp, 7000)
        self.assertEqual(res.AspectRatio, AspectRatio.W3H2)
        self.assertEqual(res.ToneEffect, ToneEffect.BAndW)


class Test_CamCaptStatus(unittest.TestCase):
    def test_RecvData(self):
        res = CamCaptStatus()
        res.decode(b"\x06\x00\x00\x01\x01\x00\x03\x0B")
        self.assertEqual(res.ImageId, 0)
        self.assertEqual(res.ImageDBHead, 0)
        self.assertEqual(res.ImageDBTail, 1)
        self.assertEqual(res.CaptStatus, CaptStatus.ShootInProgress)
        self.assertEqual(res.DestToSave, DestToSave.Both)

        res = CamCaptStatus()
        res.decode(b"\x06\x00\x00\x01\x04\x00\x03\x0E")
        self.assertEqual(res.ImageId, 0)
        self.assertEqual(res.ImageDBHead, 0)
        self.assertEqual(res.ImageDBTail, 1)
        self.assertEqual(res.CaptStatus, CaptStatus.ImageGenInProgress)
        self.assertEqual(res.DestToSave, DestToSave.Both)


class Test_PictFileInfo2(unittest.TestCase):
    def test_RecvData(self):
        res = PictFileInfo2()
        res.decode(
            b"\x38\x00\x00\x00\x01\x00\x00\x00\x0C\x00\x00\x00\x80\x05\x00\x57"
            b"\x42\x3E\x0A\x00\x24\x00\x00\x00\x2D\x00\x00\x00\x4A\x50\x47\x00"
            b"\x70\x17\xA0\x0F\x31\x30\x30\x53\x49\x47\x4D\x41\x00\x53\x44\x49"
            b"\x4D\x30\x30\x30\x31\x2E\x4A\x50\x47\x00\x03\x00")
        self.assertEqual(res.FileAddress, 0x57000580)
        self.assertEqual(res.FileSize, 0x000a3e42)
        self.assertEqual(res.PictureFormat, b"JPG")
        self.assertEqual(res.SizeX, 6000)
        self.assertEqual(res.SizeY, 4000)
        self.assertEqual(res.PathName, b"100SIGMA")
        self.assertEqual(res.FileName, b"SDIM0001.JPG")


if __name__ == '__main__':
    unittest.main()
