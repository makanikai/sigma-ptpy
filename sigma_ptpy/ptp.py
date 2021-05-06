import logging
from ptpy import PTP
from construct import (
    Array, BitsInteger, Bitwise, Bytes, Container, Default, Enum, Int16sb,
    Int16sl, Int16sn, Int16ub, Int16ul, Int16un, Int32sb, Int32sl, Int32sn,
    Int32ub, Int32ul, Int32un, Int64sb, Int64sl, Int64sn, Int64ub, Int64ul,
    Int64un, Int8sb, Int8sl, Int8sn, Int8ub, Int8ul, Int8un, Pass, Padding,
    PrefixedArray, Struct, Switch, If, String, CString, GreedyBytes, Mapping
)
from .enum import (
    DriveMode, SpecialMode, ExposureMode, AEMeteringMode, FlashType, FlashMode, FlashSetting,
    WhiteBalance, Resolution, ImageQuality, ColorSpace, ColorMode,
    BatteryKind, AFAuxLight, CaptureMode, CaptStatus, DestToSave
)

logger = logging.getLogger(__name__)

def _enum(subcon, enum_class):
    return Mapping(
        subcon,
        dict((e.value, e) for e in enum_class),
        dict((e, e.value) for e in enum_class),
        decdefault=Pass, encdefault=Pass)

class SigmaPTP(PTP):

    _DataGroup1FieldPresent = Bitwise(Struct(
        'ABSetting' / Default(BitsInteger(1), 0),
        'ABValue' / Default(BitsInteger(1), 0),
        'ExpCompensation' / Default(BitsInteger(1), 0),
        'ISOSpeed' / Default(BitsInteger(1), 0),
        'ISOAuto' / Default(BitsInteger(1), 0),
        'ProgramShift' / Default(BitsInteger(1), 0),
        'Aperture' / Default(BitsInteger(1), 0),
        'ShutterSpeed' / Default(BitsInteger(1), 0),
        '_Reserved0' / Default(BitsInteger(1), 0),
        'ExpCompExcludeAB' / Default(BitsInteger(1), 0),
        'ABShotRemainNumber' / Default(BitsInteger(1), 0),
        'BatteryState' / Default(BitsInteger(1), 0),
        'CurrentLensFocalLength' / Default(BitsInteger(1), 0),
        'MediaStatus' / Default(BitsInteger(1), 0),
        'MediaFreeSpace' / Default(BitsInteger(1), 0),
        'FrameBufferState' / Default(BitsInteger(1), 0),
    ))
    _DataGroup2FieldPresent = Bitwise(Struct(
        '_Reserved3' / Default(BitsInteger(1), 0),
        '_Reserved2' / Default(BitsInteger(1), 0),
        '_Reserved1' / Default(BitsInteger(1), 0),
        '_Reserved0' / Default(BitsInteger(1), 0),
        'AEMeteringMode' / Default(BitsInteger(1), 0),
        'ExposureMode' / Default(BitsInteger(1), 0),
        'SpecialMode' / Default(BitsInteger(1), 0),
        'DriveMode' / Default(BitsInteger(1), 0),
        'ImageQuality' / Default(BitsInteger(1), 0),
        'Resolution' / Default(BitsInteger(1), 0),
        'WhiteBalance' / Default(BitsInteger(1), 0),
        '_Reserved5' / Default(BitsInteger(1), 0),
        'FlashSetting' / Default(BitsInteger(1), 0),
        'FlashMode' / Default(BitsInteger(1), 0),
        '_Reserved4' / Default(BitsInteger(1), 0),
        'FlashType' / Default(BitsInteger(1), 0),
    ))
    _DataGroup3FieldPresent = Bitwise(Struct(
        'LensTeleFocalLength' / Default(BitsInteger(1), 0),
        'LensWideFocalLength' / Default(BitsInteger(1), 0),
        'BatteryKind' / Default(BitsInteger(1), 0),
        'ColorMode' / Default(BitsInteger(1), 0),
        'ColorSpace' / Default(BitsInteger(1), 0),
        '_Reserved2' / Default(BitsInteger(1), 0),
        '_Reserved1' / Default(BitsInteger(1), 0),
        '_Reserved0' / Default(BitsInteger(1), 0),
        'DestToSave' / Default(BitsInteger(1), 0),
        '_Reserved6' / Default(BitsInteger(1), 0),
        'TimerSound' / Default(BitsInteger(1), 0),
        '_Reserved5' / Default(BitsInteger(1), 0),
        '_Reserved4' / Default(BitsInteger(1), 0),
        '_Reserved3' / Default(BitsInteger(1), 0),
        'AFBeep' / Default(BitsInteger(1), 0),
        'AFAuxLight' / Default(BitsInteger(1), 0),
    ))
    _DriveMode = _enum(Int8un, DriveMode)
    _SpecialMode = _enum(Int8un, SpecialMode)
    _ExposureMode = _enum(Int8un, ExposureMode)
    _AEMeteringMode = _enum(Int8un, AEMeteringMode)
    _FlashType = _enum(Int8un, FlashType)
    _FlashMode = _enum(Int8un, FlashMode)
    _FlashSetting = _enum(Int8un, FlashSetting)
    _WhiteBalance = _enum(Int8un, WhiteBalance)
    _Resolution = _enum(Int8un, Resolution)
    _ImageQuality = _enum(Int8un, ImageQuality)
    _ColorSpace = _enum(Int8un, ColorSpace)
    _ColorMode = _enum(Int8un, ColorMode)
    _BatteryKind = _enum(Int8un, BatteryKind)
    _AFAuxLight = _enum(Int8un, AFAuxLight)
    _CaptureMode = _enum(Int8un, CaptureMode)
    _CaptStatus = _enum(Int16ul, CaptStatus)
    _DestToSave = _enum(Int8un, DestToSave)

    def __init__(self, *args, **kwargs):
        logger.debug("Init SigmaPTP")

        self._CamDataGroup1 = Struct(
            '_Header' / Default(Int8un, 0), # arbitrary value for parity
            'FieldPresent' / self._DataGroup1FieldPresent,
            'ShutterSpeed' / Default(If(lambda x: x.FieldPresent.ShutterSpeed == 1, Int8un), 0),
            'Aperture' / Default(If(lambda x: x.FieldPresent.Aperture == 1, Int8un), 0),
            'ProgramShift' / Default(If(lambda x: x.FieldPresent.ProgramShift == 1, Int8sn), 0),
            'ISOAuto' / Default(If(lambda x: x.FieldPresent.ISOAuto == 1, Int8un), 0),
            'ISOSpeed' / Default(If(lambda x: x.FieldPresent.ISOSpeed == 1, Int8un), 0),
            'ExpCompensation' / Default(If(lambda x: x.FieldPresent.ExpCompensation == 1, Int8un), 0),
            'ABValue' / Default(If(lambda x: x.FieldPresent.ABValue == 1, Int8un), 0),
            'ABSetting' / Default(If(lambda x: x.FieldPresent.ABSetting == 1, Int8un), 0),
            'FrameBufferState' / Default(If(lambda x: x.FieldPresent.FrameBufferState == 1, Int8un), 0),
            'MediaFreeSpace' / Default(If(lambda x: x.FieldPresent.MediaFreeSpace == 1, Int16un), 0),
            'MediaStatus' / Default(If(lambda x: x.FieldPresent.MediaStatus == 1, Int8un), 0),
            'CurrentLensFocalLength' / Default(If(lambda x: x.FieldPresent.CurrentLensFocalLength == 1, Int16un), 0),
            'BatteryState' / Default(If(lambda x: x.FieldPresent.BatteryState == 1, Int8un), 0),
            'ABShotRemainNumber' / Default(If(lambda x: x.FieldPresent.ABShotRemainNumber == 1, Int8un), 0),
            'ExpCompExcludeAB' / Default(If(lambda x: x.FieldPresent.ExpCompExcludeAB == 1, Int8un), 0),
            '_Reserved0' / Default(If(lambda x: x.FieldPresent._Reserved0 == 1, Int8un), 0),
            '_Parity' / Default(Int8un, 0)
        )

        self._CamDataGroup2 = Struct(
            '_Header' / Default(Int8un, 0), # arbitrary value for parity
            'FieldPresent' / self._DataGroup2FieldPresent,
            'DriveMode' / Default(If(lambda x: x.FieldPresent.DriveMode == 1, self._DriveMode), 0),
            'SpecialMode' / Default(If(lambda x: x.FieldPresent.SpecialMode == 1, self._SpecialMode), 0),
            'ExposureMode' / Default(If(lambda x: x.FieldPresent.ExposureMode == 1, self._ExposureMode), 0),
            'AEMeteringMode' / Default(If(lambda x: x.FieldPresent.AEMeteringMode == 1, self._AEMeteringMode), 0),
            '_Reserved0' / Default(If(lambda x: x.FieldPresent._Reserved0 == 1, Int8un), 0),
            '_Reserved1' / Default(If(lambda x: x.FieldPresent._Reserved1 == 1, Int8un), 0),
            '_Reserved2' / Default(If(lambda x: x.FieldPresent._Reserved2 == 1, Int8un), 0),
            '_Reserved3' / Default(If(lambda x: x.FieldPresent._Reserved3 == 1, Int8un), 0),
            'FlashType' / Default(If(lambda x: x.FieldPresent.FlashType == 1, self._FlashType), 0),
            '_Reserved4' / Default(If(lambda x: x.FieldPresent._Reserved4 == 1, Int8un), 0),
            'FlashMode' / Default(If(lambda x: x.FieldPresent.FlashMode == 1, self._FlashMode), 0),
            'FlashSetting' / Default(If(lambda x: x.FieldPresent.FlashSetting == 1, self._FlashSetting), 0),
            '_Reserved5' / Default(If(lambda x: x.FieldPresent._Reserved5 == 1, Int8un), 0),
            'WhiteBalance' / Default(If(lambda x: x.FieldPresent.WhiteBalance == 1, self._WhiteBalance), 0),
            'Resolution' / Default(If(lambda x: x.FieldPresent.Resolution == 1, self._Resolution), 0),
            'ImageQuality' / Default(If(lambda x: x.FieldPresent.ImageQuality == 1, self._ImageQuality), 0),
            '_Parity' / Default(Int8un, 0)
        )

        self._CamDataGroup3 = Struct(
            '_Header' / Default(Int8un, 0), # arbitrary value for parity
            'FieldPresent' / self._DataGroup3FieldPresent,
            '_Reserved0' / Default(If(lambda x: x.FieldPresent._Reserved0 == 1, Int8un), 0),
            '_Reserved1' / Default(If(lambda x: x.FieldPresent._Reserved1 == 1, Int8un), 0),
            '_Reserved2' / Default(If(lambda x: x.FieldPresent._Reserved2 == 1, Int8un), 0),
            'ColorSpace' / Default(If(lambda x: x.FieldPresent.ColorSpace == 1, self._ColorSpace), 0),
            'ColorMode' / Default(If(lambda x: x.FieldPresent.ColorMode == 1, self._ColorMode), 0),
            'BatteryKind' / Default(If(lambda x: x.FieldPresent.BatteryKind == 1, self._BatteryKind), 0),
            'LensWideFocalLength' / Default(If(lambda x: x.FieldPresent.LensWideFocalLength == 1, Int16ul), 0),
            'LensTeleFocalLength' / Default(If(lambda x: x.FieldPresent.LensTeleFocalLength == 1, Int16ul), 0),
            'AFAuxLight' / Default(If(lambda x: x.FieldPresent.AFAuxLight == 1, self._AFAuxLight), 0),
            'AFBeep' / Default(If(lambda x: x.FieldPresent.AFBeep == 1, Int8un), 0),
            '_Reserved3' / Default(If(lambda x: x.FieldPresent._Reserved3 == 1, Int8un), 0),
            '_Reserved4' / Default(If(lambda x: x.FieldPresent._Reserved4 == 1, Int8un), 0),
            '_Reserved5' / Default(If(lambda x: x.FieldPresent._Reserved5 == 1, Int8un), 0),
            'TimerSound' / Default(If(lambda x: x.FieldPresent.TimerSound == 1, Int8un), 0),
            '_Reserved6' / Default(If(lambda x: x.FieldPresent._Reserved6 == 1, Int8un), 0),
            'DestToSave' / Default(If(lambda x: x.FieldPresent.DestToSave == 1, self._DestToSave), 0),
            '_Parity' / Default(Int8un, 0)
        )

        self._CamCaptStatus = Struct(
            '_Header' / Int8un, # arbitrary value for parity
            'ImageId' / Int8un,
            'ImageDBHead' / Int8un,
            'ImageDBTail' / Int8un,
            'CaptStatus' / self._CaptStatus,
            'DestToSave' / self._DestToSave,
            '_Parity' / Int8un
        )

        self._SnapCommand = Struct(
            '_Header' / Default(Int8un, 0), # arbitrary value for parity
            'CaptureMode' / self._CaptureMode,
            'CaptureAmount' / Int8un,
            '_Parity' / Default(Int8un, 0)
        )

        self._PictFileInfo2 = Struct(
            '_A' / Bytes(12), # ?
            'FileAddress' / Int32ul,
            'FileSize' / Int32ul,
            'PathNameOffset' / Int32ul,
            'FileNameOffset' / Int32ul,
            'PictureFormat' / String(4),
            'SizeX' / Int16ul,
            'SizeY' / Int16ul,
            'PathName' / CString(),
            'FileName' / CString(),
            '_C' / Bytes(2), # ?
        )

        self._BigPartialPictFile = Struct(
            'AcquiredSize' / Int32ul,
            'PartialData' / GreedyBytes
        )

        super(SigmaPTP, self).__init__(*args, **kwargs)

    def _OperationCode(self, **vendor_operations):
        return super(SigmaPTP, self)._OperationCode(
            SigmaGetCamDataGroup1=0x9012,
            SigmaGetCamDataGroup2=0x9013,
            SigmaGetCamDataGroup3=0x9014,
            SigmaGetCamCaptStatus=0x9015,
            SigmaSetCamDataGroup1=0x9016,
            SigmaSetCamDataGroup2=0x9017,
            SigmaSetCamDataGroup3=0x9018,
            SigmaSnapCommand=0x901B,
            SigmaGetBigPartialPictFile=0x9022,
            SigmaGetViewFrame=0x902B,
            SigmaGetPictFileInfo2=0x902D,
            SigmaConfigApi=0x9035,
            **vendor_operations
        )

    def _ResponseCode(self, **vendor_operations):
        return super(SigmaPTP, self)._ResponseCode(
            SigmaGetCamDataGroup1=0x9012,
            SigmaGetCamDataGroup2=0x9013,
            SigmaGetCamDataGroup3=0x9014,
            SigmaGetCamCaptStatus=0x9015,
            SigmaSetCamDataGroup1=0x9016,
            SigmaSetCamDataGroup2=0x9017,
            SigmaSetCamDataGroup3=0x9018,
            SigmaSnapCommand=0x901B,
            SigmaGetBigPartialPictFile=0x9022,
            SigmaGetViewFrame=0x902B,
            SigmaGetPictFileInfo2=0x902D,
            SigmaConfigApi=0x9035,
            **vendor_operations
        )
