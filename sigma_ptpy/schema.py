"""Schema definitions for the SIGMA fp series"""

from construct import (
    Adapter, Bytes, FlagsEnum,
    Int16ub, Int16ul, Int32ul, Int8un,
    Pass, Struct, If, String, CString, GreedyBytes, Mapping
)
from .enum import (
    ProgramShift, ISOAuto, ABSetting, DriveMode, SpecialMode,
    ExposureMode, AEMeteringMode, FlashType, FlashMode, FlashSetting,
    WhiteBalance, Resolution, ImageQuality, ColorSpace, ColorMode,
    BatteryKind, AFAuxLight, CaptureMode, CaptStatus, DestToSave
)


class _FixedPointValue(Adapter):
    def __init__(self, subcon, fraction_bit):
        super(_FixedPointValue, self).__init__(subcon)
        self.fraction_bit = fraction_bit
        self.__mask = (1 << fraction_bit) - 1

    def _encode(self, obj, context):
        a = int(obj) << self.fraction_bit
        b = int(obj * (self.__mask + 1)) & self.__mask
        return a | b

    def _decode(self, obj, context):
        a = obj >> self.fraction_bit
        b = float(obj & self.__mask) / (self.__mask + 1)
        return a + b


def _Enum(subcon, enum_class):
    return Mapping(
        subcon,
        dict((e.value, e) for e in enum_class),
        dict((e, e.value) for e in enum_class),
        decdefault=Pass, encdefault=Pass)


def _IfDefined(key, subcon):
    return If(lambda x: key in x.FieldPresent and x.FieldPresent[key], subcon)


_ProgramShift = _Enum(Int8un, ProgramShift)
_ISOAuto = _Enum(Int8un, ISOAuto)
_ABSetting = _Enum(Int8un, ABSetting)
_DriveMode = _Enum(Int8un, DriveMode)
_SpecialMode = _Enum(Int8un, SpecialMode)
_ExposureMode = _Enum(Int8un, ExposureMode)
_AEMeteringMode = _Enum(Int8un, AEMeteringMode)
_FlashType = _Enum(Int8un, FlashType)
_FlashMode = _Enum(Int8un, FlashMode)
_FlashSetting = _Enum(Int8un, FlashSetting)
_WhiteBalance = _Enum(Int8un, WhiteBalance)
_Resolution = _Enum(Int8un, Resolution)
_ImageQuality = _Enum(Int8un, ImageQuality)
_ColorSpace = _Enum(Int8un, ColorSpace)
_ColorMode = _Enum(Int8un, ColorMode)
_BatteryKind = _Enum(Int8un, BatteryKind)
_AFAuxLight = _Enum(Int8un, AFAuxLight)
_CaptureMode = _Enum(Int8un, CaptureMode)
_CaptStatus = _Enum(Int16ul, CaptStatus)
_DestToSave = _Enum(Int8un, DestToSave)

_CamDataGroup1FieldPresent = FlagsEnum(
    Int16ub,
    ABSetting=0x8000,
    ABValue=0x4000,
    ExpComp=0x2000,
    ISOSpeed=0x1000,
    ISOAuto=0x800,
    ProgramShift=0x400,
    Aperture=0x200,
    ShutterSpeed=0x100,
    _Reserved0=0x80,
    ExpCompExcludeAB=0x40,
    ABShotRemainNumber=0x20,
    BatteryState=0x10,
    CurrentLensFocalLength=0x8,
    MediaStatus=0x4,
    MediaFreeSpace=0x2,
    FrameBufferState=0x1,
)

_CamDataGroup1 = Struct(
    '_Header' / Int8un,  # arbitrary value for parity
    'FieldPresent' / _CamDataGroup1FieldPresent,
    'ShutterSpeed' / _IfDefined('ShutterSpeed', Int8un),
    'Aperture' / _IfDefined('Aperture', Int8un),
    'ProgramShift' / _IfDefined('ProgramShift', _ProgramShift),
    'ISOAuto' / _IfDefined('ISOAuto', _ISOAuto),
    'ISOSpeed' / _IfDefined('ISOSpeed', Int8un),
    'ExpComp' / _IfDefined('ExpComp', Int8un),
    'ABValue' / _IfDefined('ABValue', Int8un),
    'ABSetting' / _IfDefined('ABSetting', _ABSetting),
    'FrameBufferState' / _IfDefined('FrameBufferState', Int8un),
    'MediaFreeSpace' / _IfDefined('MediaFreeSpace', Int16ul),
    'MediaStatus' / _IfDefined('MediaStatus', Int8un),
    'CurrentLensFocalLength' / _IfDefined('CurrentLensFocalLength', _FixedPointValue(Int16ul, 4)),
    'BatteryState' / _IfDefined('BatteryState', Int8un),
    'ABShotRemainNumber' / _IfDefined('ABShotRemainNumber', Int8un),
    'ExpCompExcludeAB' / _IfDefined('ExpCompExcludeAB', Int8un),
    '_Reserved0' / _IfDefined('_Reserved0', Int8un),
    '_Parity' / Int8un,
)

_CamDataGroup2FieldPresent = FlagsEnum(
    Int16ub,
    _Reserved3=0x8000,
    _Reserved2=0x4000,
    _Reserved1=0x2000,
    _Reserved0=0x1000,
    AEMeteringMode=0x800,
    ExposureMode=0x400,
    SpecialMode=0x200,
    DriveMode=0x100,
    ImageQuality=0x80,
    Resolution=0x40,
    WhiteBalance=0x20,
    _Reserved5=0x10,
    FlashSetting=0x8,
    FlashMode=0x4,
    _Reserved4=0x2,
    FlashType=0x1,
)

_CamDataGroup2 = Struct(
    '_Header' / Int8un,  # arbitrary value for parity
    'FieldPresent' / _CamDataGroup2FieldPresent,
    'DriveMode' / _IfDefined('DriveMode', _DriveMode),
    'SpecialMode' / _IfDefined('SpecialMode', _SpecialMode),
    'ExposureMode' / _IfDefined('ExposureMode', _ExposureMode),
    'AEMeteringMode' / _IfDefined('AEMeteringMode', _AEMeteringMode),
    '_Reserved0' / _IfDefined('_Reserved0', Int8un),
    '_Reserved1' / _IfDefined('_Reserved1', Int8un),
    '_Reserved2' / _IfDefined('_Reserved2', Int8un),
    '_Reserved3' / _IfDefined('_Reserved3', Int8un),
    'FlashType' / _IfDefined('FlashType', _FlashType),
    '_Reserved4' / _IfDefined('_Reserved4', Int8un),
    'FlashMode' / _IfDefined('FlashMode', _FlashMode),
    'FlashSetting' / _IfDefined('FlashSetting', _FlashSetting),
    '_Reserved5' / _IfDefined('_Reserved5', Int8un),
    'WhiteBalance' / _IfDefined('WhiteBalance', _WhiteBalance),
    'Resolution' / _IfDefined('Resolution', _Resolution),
    'ImageQuality' / _IfDefined('ImageQuality', _ImageQuality),
    '_Parity' / Int8un,
)

_CamDataGroup3FieldPresent = FlagsEnum(
    Int16ub,
    LensTeleFocalLength=0x8000,
    LensWideFocalLength=0x4000,
    BatteryKind=0x2000,
    ColorMode=0x1000,
    ColorSpace=0x800,
    _Reserved2=0x400,
    _Reserved1=0x200,
    _Reserved0=0x100,
    DestToSave=0x80,
    _Reserved6=0x40,
    TimerSound=0x20,
    _Reserved5=0x10,
    _Reserved4=0x8,
    _Reserved3=0x4,
    AFBeep=0x2,
    AFAuxLight=0x1,
)

_CamDataGroup3 = Struct(
    '_Header' / Int8un,  # arbitrary value for parity
    'FieldPresent' / _CamDataGroup3FieldPresent,
    '_Reserved0' / _IfDefined('_Reserved0', Int8un),
    '_Reserved1' / _IfDefined('_Reserved1', Int8un),
    '_Reserved2' / _IfDefined('_Reserved2', Int8un),
    'ColorSpace' / _IfDefined('ColorSpace', _ColorSpace),
    'ColorMode' / _IfDefined('ColorMode', _ColorMode),
    'BatteryKind' / _IfDefined('BatteryKind', _BatteryKind),
    'LensWideFocalLength' / _IfDefined('LensWideFocalLength', _FixedPointValue(Int16ul, 4)),
    'LensTeleFocalLength' / _IfDefined('LensTeleFocalLength', _FixedPointValue(Int16ul, 4)),
    'AFAuxLight' / _IfDefined('AFAuxLight', _AFAuxLight),
    'AFBeep' / _IfDefined('AFBeep', Int8un),
    '_Reserved3' / _IfDefined('_Reserved3', Int8un),
    '_Reserved4' / _IfDefined('_Reserved4', Int8un),
    '_Reserved5' / _IfDefined('_Reserved5', Int8un),
    'TimerSound' / _IfDefined('TimerSound', Int8un),
    '_Reserved6' / _IfDefined('_Reserved6', Int8un),
    'DestToSave' / _IfDefined('DestToSave', _DestToSave),
    '_Parity' / Int8un
)

_CamCaptStatus = Struct(
    '_Header' / Int8un,  # arbitrary value for parity
    'ImageId' / Int8un,
    'ImageDBHead' / Int8un,
    'ImageDBTail' / Int8un,
    'CaptStatus' / _CaptStatus,
    'DestToSave' / _DestToSave,
    '_Parity' / Int8un
)

_SnapCommand = Struct(
    '_Header' / Int8un,  # arbitrary value for parity
    'CaptureMode' / _CaptureMode,
    'CaptureAmount' / Int8un,
    '_Parity' / Int8un,
)

_PictFileInfo2 = Struct(
    '_Unknown0' / Bytes(12),  # ?
    'FileAddress' / Int32ul,
    'FileSize' / Int32ul,
    'PathNameOffset' / Int32ul,
    'FileNameOffset' / Int32ul,
    'PictureFormat' / String(4),
    'SizeX' / Int16ul,
    'SizeY' / Int16ul,
    'PathName' / CString(),
    'FileName' / CString(),
    '_Unknown1' / Bytes(2),  # ?
)

_BigPartialPictFile = Struct(
    'AcquiredSize' / Int32ul,
    'PartialData' / GreedyBytes
)
