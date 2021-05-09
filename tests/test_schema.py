import unittest
from construct import Container
from sigma_ptpy.enum import (
    DirectoryType,
    DriveMode, SpecialMode, ExposureMode, AEMeteringMode, FlashMode, FlashSetting,
    WhiteBalance, Resolution, ImageQuality, ColorSpace, ColorMode,
    BatteryKind, AFAuxLight, CaptStatus, DestToSave,
    DCCropMode, LVMagnifyRatio, HighISOExt, ContShootSpeed, HDR,
    DNGQuality, LOCDistortion, LOCChromaticAbberation, LOCDiffraction,
    LOCVignetting, LOCColorShade, LOCColorShadeAcq, EImageStab,
    ToneEffect, AspectRatio
)
from sigma_ptpy.schema import (
    _CamDataGroup1, _CamDataGroup2, _CamDataGroup3, _CamDataGroup4, _CamDataGroup5,
    _DirectoryEntryArray, _CamCaptStatus, _PictFileInfo2,
    _decode_directory_entry
)


class Test_CamDataGroup1(unittest.TestCase):
    def test_ShutterSpeed(self):
        res = _CamDataGroup1.parse(b"\x03\x01\x00\x10\x14")
        self.assertEqual(res.FieldPresent.ShutterSpeed, 1)
        self.assertEqual(res.ShutterSpeed, 16)  # SS=30s

        res = _CamDataGroup1.parse(b"\x03\x01\x00\x5B\x5F")
        self.assertEqual(res.FieldPresent.ShutterSpeed, 1)
        self.assertEqual(res.ShutterSpeed, 91)  # SS=1/20s

    def test_Aperture(self):
        res = _CamDataGroup1.parse(b"\x03\x02\x00\x20\x25")
        self.assertEqual(res.FieldPresent.Aperture, 1)
        self.assertEqual(res.Aperture, 32)  # F=2.8

        res = _CamDataGroup1.parse(b"\x03\x02\x00\x28\x2D")
        self.assertEqual(res.FieldPresent.Aperture, 1)
        self.assertEqual(res.Aperture, 40)  # F=4.0

    def test_ISOAuto(self):
        res = _CamDataGroup1.parse(b"\x03\x08\x00\x00\x0B")
        self.assertEqual(res.FieldPresent.ISOAuto, 1)
        self.assertEqual(res.ISOAuto, 0)

        res = _CamDataGroup1.parse(b"\x03\x08\x00\x01\x0C")
        self.assertEqual(res.FieldPresent.ISOAuto, 1)
        self.assertEqual(res.ISOAuto, 1)

    def test_ISOSpeed(self):
        res = _CamDataGroup1.parse(b"\x03\x10\x00\x20\x33")
        self.assertEqual(res.FieldPresent.ISOSpeed, 1)
        self.assertEqual(res.ISOSpeed, 32)  # ISO=100

        res = _CamDataGroup1.parse(b"\x03\x10\x00\x48\x5B")
        self.assertEqual(res.FieldPresent.ISOSpeed, 1)
        self.assertEqual(res.ISOSpeed, 72)  # ISO=3200

    def test_RecvData(self):
        res = _CamDataGroup1.parse(b"\x13\xff\x7f\x20\x20\x00\x01\xf8\x00\x00\x01\tk\x03\x01\xd0\x02\x08\x00\x00\x1d")

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
        self.assertEqual(res.FieldPresent.ExpComp, 1)
        self.assertEqual(res.ExpComp, 0)
        self.assertEqual(res.FieldPresent.ABValue, 1)
        self.assertEqual(res.ABValue, 0)
        self.assertEqual(res.FieldPresent.ABSetting, 1)
        self.assertEqual(res.ABSetting, 1)

        self.assertEqual(res.FieldPresent._Reserved0, 0)
        self.assertEqual(res.FieldPresent.FrameBufferState, 1)
        self.assertEqual(res.FrameBufferState, 0x09)
        self.assertEqual(res.FieldPresent.MediaFreeSpace, 1)
        self.assertEqual(res.MediaFreeSpace, 0x036B)
        self.assertEqual(res.FieldPresent.MediaStatus, 1)
        self.assertEqual(res.MediaStatus, 0x01)
        self.assertEqual(res.FieldPresent.CurrentLensFocalLength, 1)
        self.assertEqual(res.CurrentLensFocalLength, 45.0)
        self.assertEqual(res.FieldPresent.BatteryState, 1)
        self.assertEqual(res.BatteryState, 0x08)
        self.assertEqual(res.FieldPresent.ABShotRemainNumber, 1)
        self.assertEqual(res.ABShotRemainNumber, 0)
        self.assertEqual(res.FieldPresent.ExpCompExcludeAB, 1)
        self.assertEqual(res.ExpCompExcludeAB, 0)


class Test_CamDataGroup2(unittest.TestCase):
    def test_ExposureMode(self):
        res = _CamDataGroup2.parse(b"\x03\x04\x00\x04\x0B")
        self.assertEqual(res.FieldPresent.ExposureMode, 1)
        self.assertEqual(res.ExposureMode, ExposureMode.Manual)

    def test_WhiteBalance(self):
        res = _CamDataGroup2.parse(b"\x03\x00\x20\x01\x24")
        self.assertEqual(res.FieldPresent.WhiteBalance, 1)
        self.assertEqual(res.WhiteBalance, WhiteBalance.Auto)

        res = _CamDataGroup2.parse(b"\x03\x00\x20\x06\x29")
        self.assertEqual(res.FieldPresent.WhiteBalance, 1)
        self.assertEqual(res.WhiteBalance, WhiteBalance.Fluorescent)

    def test_RecvData(self):
        res = _CamDataGroup2.parse(b"\x0e\x3f\xfc\x07\x02\x04\x01\x00\x03\x00\x00\x00\x01\x01\x10l")

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


class Test_CamDataGroup3(unittest.TestCase):
    def test_RecvData(self):
        res = _CamDataGroup3.parse(b"\x10\xff\xa3\x00\x00\x00\x01\x03\x02\x00\xd0\x00\x00\x02\x05\x05\x02\x96")

        self.assertEqual(res.FieldPresent.ColorSpace, 1)
        self.assertEqual(res.ColorSpace, ColorSpace.sRGB)
        self.assertEqual(res.FieldPresent.ColorMode, 1)
        self.assertEqual(res.ColorMode, ColorMode.Standard)
        self.assertEqual(res.FieldPresent.BatteryKind, 1)
        self.assertEqual(res.BatteryKind, BatteryKind.ACAdapter)
        self.assertEqual(res.FieldPresent.LensWideFocalLength, 1)
        self.assertEqual(res.LensWideFocalLength, 0xd00 + 0.0)
        self.assertEqual(res.FieldPresent.LensTeleFocalLength, 1)
        self.assertEqual(res.LensTeleFocalLength, 0x0000)
        self.assertEqual(res.FieldPresent.AFAuxLight, 1)
        self.assertEqual(res.AFAuxLight, AFAuxLight.Off)
        self.assertEqual(res.FieldPresent.AFBeep, 1)
        self.assertEqual(res.AFBeep, 0x05)
        self.assertEqual(res.FieldPresent.TimerSound, 1)
        self.assertEqual(res.TimerSound, 0x05)
        self.assertEqual(res.FieldPresent.DestToSave, 1)
        self.assertEqual(res.DestToSave, DestToSave.InComputer)


class Test_CamDataGroup4(unittest.TestCase):
    def test_RecvData(self):
        res = _CamDataGroup4.parse(b"\x11\xf0\x3f\x00\x03\x01\x03\xff\x0e\x00\x01\x01\x02\x01\xfe\x02\x02\x05\x60")

        self.assertEqual(res.FieldPresent.DCCropMode, 1)
        self.assertEqual(res.DCCropMode, DCCropMode.Auto)
        self.assertEqual(res.FieldPresent.LVMagnifyRatio, 1)
        self.assertEqual(res.LVMagnifyRatio, LVMagnifyRatio.x8)
        self.assertEqual(res.FieldPresent.HighISOExt, 1)
        self.assertEqual(res.HighISOExt, HighISOExt.Off)
        self.assertEqual(res.FieldPresent.ContShootSpeed, 1)
        self.assertEqual(res.ContShootSpeed, ContShootSpeed.Low)
        self.assertEqual(res.FieldPresent.HDR, 1)
        self.assertEqual(res.HDR, HDR.Off)
        self.assertEqual(res.FieldPresent.DNGQuality, 1)
        self.assertEqual(res.DNGQuality, DNGQuality.Q14bit)
        self.assertEqual(res.FieldPresent.FillLight, 1)
        self.assertEqual(res.FillLight, 0x00)
        self.assertEqual(res.FieldPresent.LOC, 1)
        self.assertEqual(res.LOCDistortion, LOCDistortion.Auto)
        self.assertEqual(res.LOCChromaticAbberation, LOCChromaticAbberation.Auto)
        self.assertEqual(res.LOCDiffraction, LOCDiffraction.Off)
        self.assertEqual(res.LOCVignetting, LOCVignetting.Auto)
        self.assertEqual(res.LOCColorShade, LOCColorShade.Off)
        self.assertEqual(res.LOCColorShadeAcq, LOCColorShadeAcq.Off)
        self.assertEqual(res.FieldPresent.EImageStab, 1)
        self.assertEqual(res.EImageStab, EImageStab.Off)
        self.assertEqual(res.FieldPresent.ShutterSound, 1)
        self.assertEqual(res.ShutterSound, 5)


class Test_CamDataGroup5(unittest.TestCase):
    def test_RecvData(self):
        res = _CamDataGroup5.parse(b"\x0c\x2b\x00\x0a\x00\x01\x00\x00\x01\x58\x1b\x03\x01\xba")

        self.assertEqual(res.FieldPresent.IntervalTimer, 1)
        self.assertEqual(res.IntervalTimerSecond, 10)
        self.assertEqual(res.IntervalTimerFrame, 1)
        self.assertEqual(res.IntervalTimerSecondRemain, 0)
        self.assertEqual(res.IntervalTimerFrameRemain, 1)
        self.assertEqual(res.FieldPresent.ColorTemp, 1)
        self.assertEqual(res.ColorTemp, 7000)
        self.assertEqual(res.FieldPresent.AspectRatio, 1)
        self.assertEqual(res.AspectRatio, AspectRatio.W3H2)
        self.assertEqual(res.FieldPresent.ToneEffect, 1)
        self.assertEqual(res.ToneEffect, ToneEffect.BAndW)
        self.assertEqual(res.FieldPresent.AFAuxLightEF, 0)


class Test_DirectoryEntryArray(unittest.TestCase):
    def test_ApiConfig(self):
        rawdata = \
            b"\x4a\x00\x00\x00\x04\x00\x00\x00\x01\x00\x02\x00\x09\x00\x00\x00\x3c\x00\x00\x00\x02" \
            b"\x00\x02\x00\x09\x00\x00\x00\x45\x00\x00\x00\x03\x00\x02\x00\x04\x00\x00\x00\x56\x38" \
            b"\x32\x00\x05\x00\x0b\x00\x01\x00\x00\x00\x52\xb8\x9e\x3f\x00\x00\x00\x00\x53\x49\x47" \
            b"\x4d\x41\x20\x66\x70\x00\x39\x31\x34\x30\x32\x30\x38\x31\x00\xa9"
        res = _DirectoryEntryArray.parse(rawdata)

        self.assertEqual(res.DataLength, 0x4a)
        self.assertEqual(res.DirectoryCount, 4)
        self.assertEqual(len(res.Entries), 5)

        self.assertEqual(res.Entries[0].Tag, 1)
        self.assertEqual(res.Entries[0].Type, DirectoryType.String)
        self.assertEqual(res.Entries[0].Count, 9)
        self.assertEqual(res.Entries[0].Value, b'\x3c\x00\x00\x00')

        self.assertEqual(res.Entries[1].Tag, 2)
        self.assertEqual(res.Entries[1].Type, DirectoryType.String)
        self.assertEqual(res.Entries[1].Count, 9)
        self.assertEqual(res.Entries[1].Value, b'\x45\x00\x00\x00')

        self.assertEqual(res.Entries[2].Tag, 3)
        self.assertEqual(res.Entries[2].Type, DirectoryType.String)
        self.assertEqual(res.Entries[2].Count, 4)
        self.assertEqual(res.Entries[2].Value, b'\x56\x38\x32\x00')

        self.assertEqual(res.Entries[3].Tag, 5)
        self.assertEqual(res.Entries[3].Type, DirectoryType.Float32)
        self.assertEqual(res.Entries[3].Count, 1)
        self.assertEqual(res.Entries[3].Value, b'\x52\xb8\x9e\x3f')

    def test_CamDataGroupFocus(self):
        res = _DirectoryEntryArray.parse(
            b"\x94\x00\x00\x00\x0b\x00\x00\x00\x01\x00\x01\x00\x01\x00\x00\x00\x03"
            b"\x00\x00\x00\x02\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x03\x00"
            b"\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x04\x00\x01\x00\x01\x00\x00"
            b"\x00\x00\x00\x00\x00\x0a\x00\x01\x00\x01\x00\x00\x00\x01\x00\x00\x00"
            b"\x0b\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x01\x00\x01"
            b"\x00\x00\x00\x00\x00\x00\x00\x0d\x00\x07\x00\x04\x00\x00\x00\x54\x01"
            b"\x00\x02\x0e\x00\x07\x00\x08\x00\x00\x00\x90\x00\x00\x00\x33\x00\x01"
            b"\x00\x01\x00\x00\x00\x00\x00\x00\x00")

        self.assertEqual(res.DataLength, 0x94)
        self.assertEqual(res.DirectoryCount, 11)
        self.assertEqual(len(res.Entries), 10)  # DirectoryCount is possibly wrong.

        self.assertEqual(res.Entries[0].Tag, 1)
        self.assertEqual(res.Entries[0].Type, DirectoryType.UInt8)
        self.assertEqual(res.Entries[0].Count, 1)
        self.assertEqual(res.Entries[0].Value, b'\x03\x00\x00\x00')

        self.assertEqual(res.Entries[1].Tag, 2)
        self.assertEqual(res.Entries[1].Type, DirectoryType.UInt8)
        self.assertEqual(res.Entries[1].Count, 1)
        self.assertEqual(res.Entries[1].Value, b'\x00\x00\x00\x00')

        self.assertEqual(res.Entries[2].Tag, 3)
        self.assertEqual(res.Entries[2].Type, DirectoryType.UInt8)
        self.assertEqual(res.Entries[2].Count, 1)
        self.assertEqual(res.Entries[2].Value, b'\x00\x00\x00\x00')

        self.assertEqual(res.Entries[3].Tag, 4)
        self.assertEqual(res.Entries[3].Type, DirectoryType.UInt8)
        self.assertEqual(res.Entries[3].Count, 1)
        self.assertEqual(res.Entries[3].Value, b'\x00\x00\x00\x00')

        self.assertEqual(res.Entries[4].Tag, 0x0a)
        self.assertEqual(res.Entries[4].Type, DirectoryType.UInt8)
        self.assertEqual(res.Entries[4].Count, 1)
        self.assertEqual(res.Entries[4].Value, b'\x01\x00\x00\x00')

        self.assertEqual(res.Entries[5].Tag, 0x0b)
        self.assertEqual(res.Entries[5].Type, DirectoryType.UInt8)
        self.assertEqual(res.Entries[5].Count, 1)
        self.assertEqual(res.Entries[5].Value, b'\x00\x00\x00\x00')

        self.assertEqual(res.Entries[6].Tag, 0x0c)
        self.assertEqual(res.Entries[6].Type, DirectoryType.UInt8)
        self.assertEqual(res.Entries[6].Count, 1)
        self.assertEqual(res.Entries[6].Value, b'\x00\x00\x00\x00')

        self.assertEqual(res.Entries[7].Tag, 0x0d)
        self.assertEqual(res.Entries[7].Type, DirectoryType.Any8)
        self.assertEqual(res.Entries[7].Count, 4)
        self.assertEqual(res.Entries[7].Value, b'\x54\x01\x00\x02')

        self.assertEqual(res.Entries[8].Tag, 0x0e)
        self.assertEqual(res.Entries[8].Type, DirectoryType.Any8)
        self.assertEqual(res.Entries[8].Count, 8)
        self.assertEqual(res.Entries[8].Value, b'\x90\x00\x00\x00')

        self.assertEqual(res.Entries[9].Tag, 0x33)
        self.assertEqual(res.Entries[9].Type, DirectoryType.UInt8)
        self.assertEqual(res.Entries[9].Count, 1)
        self.assertEqual(res.Entries[9].Value, b'\x00\x00\x00\x00')


class Test__decode_directory_entries(unittest.TestCase):
    def test_UInt8(self):
        actual = _decode_directory_entry(Container(
            Type=DirectoryType.UInt8,
            Count=1,
            Value=b'\x03\x00\x00\x00'
        ), None)
        self.assertEqual(actual, [3])

        actual = _decode_directory_entry(Container(
            Type=DirectoryType.UInt8,
            Count=5,
            Value=b'\x01\x00\x00\x00'
        ), b"\x00\x01\x02\03\x04\x05")
        self.assertEqual(actual, [1, 2, 3, 4, 5])

    def test_UInt16(self):
        actual = _decode_directory_entry(Container(
            Type=DirectoryType.UInt16,
            Count=1,
            Value=b'\x03\x01\x00\x00'
        ), None)
        self.assertEqual(actual, [0x0103])

        actual = _decode_directory_entry(Container(
            Type=DirectoryType.UInt16,
            Count=3,
            Value=b'\x01\x00\x00\x00'
        ), b"\x00\x01\x02\03\x04\x05\x06")
        self.assertEqual(actual, [0x0201, 0x0403, 0x0605])

    def test_Float32(self):
        actual = _decode_directory_entry(Container(
            Type=DirectoryType.Float32,
            Count=1,
            Value=b"\x52\xb8\x9e\x3f"
        ), None)
        self.assertEqual(len(actual), 1)
        self.assertAlmostEqual(actual[0], 1.2400000095367432)

    def test_String(self):
        actual = _decode_directory_entry(Container(
            Type=DirectoryType.String,
            Count=4,
            Value=b"\x56\x38\x32\x00"
        ), None)
        self.assertEqual(actual, "V82")

        rawdata = \
            b"\x4a\x00\x00\x00\x04\x00\x00\x00\x01\x00\x02\x00\x09\x00\x00\x00\x3c\x00\x00\x00\x02" \
            b"\x00\x02\x00\x09\x00\x00\x00\x45\x00\x00\x00\x03\x00\x02\x00\x04\x00\x00\x00\x56\x38" \
            b"\x32\x00\x05\x00\x0b\x00\x01\x00\x00\x00\x52\xb8\x9e\x3f\x00\x00\x00\x00\x53\x49\x47" \
            b"\x4d\x41\x20\x66\x70\x00\x39\x31\x34\x30\x32\x30\x38\x31\x00\xa9"
        actual = _decode_directory_entry(Container(
            Type=DirectoryType.String,
            Count=9,
            Value=b"\x3c\x00\x00\x00"
        ), rawdata)
        self.assertEqual(actual, "SIGMA fp")


class Test_CamCaptStatus(unittest.TestCase):
    def test_RecvData(self):
        res = _CamCaptStatus.parse(b"\x06\x00\x00\x01\x01\x00\x03\x0B")
        self.assertEqual(res.ImageId, 0)
        self.assertEqual(res.ImageDBHead, 0)
        self.assertEqual(res.ImageDBTail, 1)
        self.assertEqual(res.CaptStatus, CaptStatus.ShootInProgress)
        self.assertEqual(res.DestToSave, DestToSave.Both)

        res = _CamCaptStatus.parse(b"\x06\x00\x00\x01\x04\x00\x03\x0E")
        self.assertEqual(res.ImageId, 0)
        self.assertEqual(res.ImageDBHead, 0)
        self.assertEqual(res.ImageDBTail, 1)
        self.assertEqual(res.CaptStatus, CaptStatus.ImageGenInProgress)
        self.assertEqual(res.DestToSave, DestToSave.Both)


class Test_PictFileInfo2(unittest.TestCase):
    def test_RecvData(self):
        res = _PictFileInfo2.parse((
            b"\x38\x00\x00\x00\x01\x00\x00\x00\x0C\x00\x00\x00\x80\x05\x00\x57"
            b"\x42\x3E\x0A\x00\x24\x00\x00\x00\x2D\x00\x00\x00\x4A\x50\x47\x00"
            b"\x70\x17\xA0\x0F\x31\x30\x30\x53\x49\x47\x4D\x41\x00\x53\x44\x49"
            b"\x4D\x30\x30\x30\x31\x2E\x4A\x50\x47\x00\x03\x00"))
        self.assertEqual(res.FileAddress, 0x57000580)
        self.assertEqual(res.FileSize, 0x000a3e42)
        self.assertEqual(res.PictureFormat, b"JPG")
        self.assertEqual(res.SizeX, 6000)
        self.assertEqual(res.SizeY, 4000)
        self.assertEqual(res.PathName, b"100SIGMA")
        self.assertEqual(res.FileName, b"SDIM0001.JPG")


if __name__ == '__main__':
    unittest.main()
