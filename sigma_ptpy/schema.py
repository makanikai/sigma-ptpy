"""Schema definitions for the SIGMA fp series"""

import struct
from construct import (
    Adapter, Bytes, FlagsEnum,
    Int16ub, Int16ul, Int32ul, Int8un,
    Pass, Struct, If, String, CString, GreedyBytes, GreedyRange, Mapping
)
from .enum import (
    DirectoryType,
    ProgramShift, ISOAuto, ABSetting, DriveMode, SpecialMode,
    ExposureMode, AEMeteringMode, FlashType, FlashMode, FlashSetting,
    WhiteBalance, Resolution, ImageQuality, ColorSpace, ColorMode,
    BatteryKind, AFAuxLight, CaptureMode, CaptStatus, DestToSave,
    DCCropMode, LVMagnifyRatio, HighISOExt, ContShootSpeed, HDR,
    DNGQuality, LOCDistortion, LOCChromaticAbberation, LOCDiffraction,
    LOCVignetting, LOCColorShade, LOCColorShadeAcq, EImageStab,
    AspectRatio, ToneEffect, AFAuxLightEF
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
    'ProgramShift' / _IfDefined('ProgramShift', _Enum(Int8un, ProgramShift)),
    'ISOAuto' / _IfDefined('ISOAuto', _Enum(Int8un, ISOAuto)),
    'ISOSpeed' / _IfDefined('ISOSpeed', Int8un),
    'ExpComp' / _IfDefined('ExpComp', Int8un),
    'ABValue' / _IfDefined('ABValue', Int8un),
    'ABSetting' / _IfDefined('ABSetting', _Enum(Int8un, ABSetting)),
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
    'DriveMode' / _IfDefined('DriveMode', _Enum(Int8un, DriveMode)),
    'SpecialMode' / _IfDefined('SpecialMode', _Enum(Int8un, SpecialMode)),
    'ExposureMode' / _IfDefined('ExposureMode', _Enum(Int8un, ExposureMode)),
    'AEMeteringMode' / _IfDefined('AEMeteringMode', _Enum(Int8un, AEMeteringMode)),
    '_Reserved0' / _IfDefined('_Reserved0', Int8un),
    '_Reserved1' / _IfDefined('_Reserved1', Int8un),
    '_Reserved2' / _IfDefined('_Reserved2', Int8un),
    '_Reserved3' / _IfDefined('_Reserved3', Int8un),
    'FlashType' / _IfDefined('FlashType', _Enum(Int8un, FlashType)),
    '_Reserved4' / _IfDefined('_Reserved4', Int8un),
    'FlashMode' / _IfDefined('FlashMode', _Enum(Int8un, FlashMode)),
    'FlashSetting' / _IfDefined('FlashSetting', _Enum(Int8un, FlashSetting)),
    '_Reserved5' / _IfDefined('_Reserved5', Int8un),
    'WhiteBalance' / _IfDefined('WhiteBalance', _Enum(Int8un, WhiteBalance)),
    'Resolution' / _IfDefined('Resolution', _Enum(Int8un, Resolution)),
    'ImageQuality' / _IfDefined('ImageQuality', _Enum(Int8un, ImageQuality)),
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
    'ColorSpace' / _IfDefined('ColorSpace', _Enum(Int8un, ColorSpace)),
    'ColorMode' / _IfDefined('ColorMode', _Enum(Int8un, ColorMode)),
    'BatteryKind' / _IfDefined('BatteryKind', _Enum(Int8un, BatteryKind)),
    'LensWideFocalLength' / _IfDefined('LensWideFocalLength', _FixedPointValue(Int16ul, 4)),
    'LensTeleFocalLength' / _IfDefined('LensTeleFocalLength', _FixedPointValue(Int16ul, 4)),
    'AFAuxLight' / _IfDefined('AFAuxLight', _Enum(Int8un, AFAuxLight)),
    'AFBeep' / _IfDefined('AFBeep', Int8un),
    '_Reserved3' / _IfDefined('_Reserved3', Int8un),
    '_Reserved4' / _IfDefined('_Reserved4', Int8un),
    '_Reserved5' / _IfDefined('_Reserved5', Int8un),
    'TimerSound' / _IfDefined('TimerSound', Int8un),
    '_Reserved6' / _IfDefined('_Reserved6', Int8un),
    'DestToSave' / _IfDefined('DestToSave', _Enum(Int8un, DestToSave)),
    '_Parity' / Int8un
)

_CamDataGroup4FieldPresent = FlagsEnum(
    Int16ub,
    ContShootSpeed=0x8000,
    HighISOExt=0x4000,
    LVMagnifyRatio=0x2000,
    DCCropMode=0x1000,
    _Reserved3=0x800,
    _Reserved2=0x400,
    _Reserved1=0x200,
    _Reserved0=0x100,
    _Reserved5=0x80,
    _Reserved6=0x40,
    ShutterSound=0x20,
    EImageStab=0x10,
    LOC=0x8,
    FillLight=0x4,
    DNGQuality=0x2,
    HDR=0x1,
)

_CamDataGroup4 = Struct(
    '_Header' / Int8un,  # arbitrary value for parity
    'FieldPresent' / _CamDataGroup4FieldPresent,
    '_Reserved0' / _IfDefined('_Reserved0', Int8un),
    '_Reserved1' / _IfDefined('_Reserved1', Int8un),
    '_Reserved2' / _IfDefined('_Reserved2', Int8un),
    '_Reserved3' / _IfDefined('_Reserved3', Int8un),
    'DCCropMode' / _IfDefined('DCCropMode', _Enum(Int8un, DCCropMode)),
    'LVMagnifyRatio' / _IfDefined('LVMagnifyRatio', _Enum(Int8un, LVMagnifyRatio)),
    'HighISOExt' / _IfDefined('HighISOExt', _Enum(Int8un, HighISOExt)),
    'ContShootSpeed' / _IfDefined('ContShootSpeed', _Enum(Int8un, ContShootSpeed)),
    'HDR' / _IfDefined('HDR', _Enum(Int8un, HDR)),
    'DNGQuality' / _IfDefined('DNGQuality', _Enum(Int8un, DNGQuality)),
    'FillLight' / _IfDefined('FillLight', Int8un),
    'LOCDistortion' / _IfDefined('LOC', _Enum(Int8un, LOCDistortion)),
    'LOCChromaticAbberation' / _IfDefined('LOC', _Enum(Int8un, LOCChromaticAbberation)),
    'LOCDiffraction' / _IfDefined('LOC', _Enum(Int8un, LOCDiffraction)),
    'LOCVignetting' / _IfDefined('LOC', _Enum(Int8un, LOCVignetting)),
    'LOCColorShade' / _IfDefined('LOC', _Enum(Int8un, LOCColorShade)),
    'LOCColorShadeAcq' / _IfDefined('LOC', _Enum(Int8un, LOCColorShadeAcq)),
    'EImageStab' / _IfDefined('EImageStab', _Enum(Int8un, EImageStab)),
    'ShutterSound' / _IfDefined('ShutterSound', Int8un),
    '_Reserved4' / _IfDefined('_Reserved4', Int8un),
    '_Reserved5' / _IfDefined('_Reserved5', Int8un),
    '_Parity' / Int8un
)

_CamDataGroup5FieldPresent = FlagsEnum(
    Int16ub,
    _Reserved3=0x8000,
    _Reserved2=0x4000,
    ToneEffect=0x2000,
    _Reservec1=0x1000,
    AspectRatio=0x800,
    _Reserved0=0x400,
    ColorTemp=0x200,
    IntervalTimer=0x100,
    AFAuxLightEF=0x80,
    _Reserved10=0x40,
    _Reserved9=0x20,
    _Reserved8=0x10,
    _Reserved7=0x8,
    _Reserved6=0x4,
    _Reserved5=0x2,
    _Reserved4=0x1,
)

_CamDataGroup5 = Struct(
    '_Header' / Int8un,  # arbitrary value for parity
    'FieldPresent' / _CamDataGroup5FieldPresent,
    'IntervalTimerSecond' / _IfDefined('IntervalTimer', Int16ul),
    'IntervalTimerFrame' / _IfDefined('IntervalTimer', Int8un),
    'IntervalTimerSecondRemain' / _IfDefined('IntervalTimer', Int16ul),
    'IntervalTimerFrameRemain' / _IfDefined('IntervalTimer', Int8un),
    'ColorTemp' / _IfDefined('ColorTemp', Int16ul),
    '_Reserved0' / _IfDefined('_Reserved0', Int8un),
    '_Reserved1' / _IfDefined('_Reserved1', Int8un),
    'AspectRatio' / _IfDefined('AspectRatio', _Enum(Int8un, AspectRatio)),
    '_Reserved2' / _IfDefined('_Reserved2', Int8un),
    'ToneEffect' / _IfDefined('ToneEffect', _Enum(Int8un, ToneEffect)),
    '_Reserved3' / _IfDefined('_Reserved3', Int8un),
    '_Reserved4' / _IfDefined('_Reserved4', Int8un),
    '_Reserved5' / _IfDefined('_Reserved5', Int8un),
    '_Reserved6' / _IfDefined('_Reserved6', Int8un),
    '_Reserved7' / _IfDefined('_Reserved7', Int8un),
    '_Reserved8' / _IfDefined('_Reserved8', Int8un),
    '_Reserved9' / _IfDefined('_Reserved9', Int8un),
    '_Reserved10' / _IfDefined('_Reserved10', Int8un),
    'AFAuxLightEF' / _IfDefined('AFAuxLightEF', _Enum(Int8un, AFAuxLightEF)),
    '_Parity' / Int8un
)

_CamCaptStatus = Struct(
    '_Header' / Int8un,  # arbitrary value for parity
    'ImageId' / Int8un,
    'ImageDBHead' / Int8un,
    'ImageDBTail' / Int8un,
    'CaptStatus' / _Enum(Int16ul, CaptStatus),
    'DestToSave' / _Enum(Int8un, DestToSave),
    '_Parity' / Int8un
)

_SnapCommand = Struct(
    '_Header' / Int8un,  # arbitrary value for parity
    'CaptureMode' / _Enum(Int8un, CaptureMode),
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

_DirectoryEntry = Struct(
    'Tag' / Int16ul,  # Tag. Defines the individual ID for each instruction.
    'Type' / _Enum(Int16ul, DirectoryType),  # Directory type
    'Count' / Int32ul,  # the number of elements included in the directory entry
    'Value' / Bytes(4)
    # Offset to value. If data fits in 4 bytes, enter the value; otherwise, enter the offset from
    # the reference position. (The data length position is used as the reference position.)
)

_DirectoryEntryArray = Struct(
    'DataLength' / Int32ul,
    'DirectoryCount' / Int32ul,
    'Entries' / GreedyRange(_DirectoryEntry)
)


def _decode_int(b, signed=True):
    return int.from_bytes(b, byteorder="little", signed=signed)


def _extract_payload(src, rawdata, size):
    n = src.Count * size
    if n <= 4:
        return src.Value[0:n]
    else:
        i = _decode_int(src.Value)
        return rawdata[i:i+n]


def _decode_int_array(src, rawdata, size, signed):
    b = _extract_payload(src, rawdata, size)
    return [_decode_int(b[i:i+size], signed=signed) for i in range(0, len(b), size)]


def _decode_float_array(src, rawdata, size, fmt):
    b = _extract_payload(src, rawdata, size)
    return list(struct.unpack("<" + fmt * src.Count, b))


def _decode_rational_array(src, rawdata, signed):
    b = _extract_payload(src, rawdata, 8)
    return [(_decode_int(b[i:i+4], signed=signed), _decode_int(b[i+4:i+8], signed=signed)) for i in range(0, len(b), 8)]


def _decode_directory_entry(src, rawdata):
    switch_ = {
        DirectoryType.UInt8: lambda: _decode_int_array(src, rawdata, 1, False),
        DirectoryType.Any8: lambda: _decode_int_array(src, rawdata, 1, False),
        DirectoryType.Int8: lambda: _decode_int_array(src, rawdata, 1, True),
        DirectoryType.UInt16: lambda: _decode_int_array(src, rawdata, 2, False),
        DirectoryType.Int16: lambda: _decode_int_array(src, rawdata, 2, True),
        DirectoryType.UInt32: lambda: _decode_int_array(src, rawdata, 4, False),
        DirectoryType.Int32: lambda: _decode_int_array(src, rawdata, 4, True),
        DirectoryType.Float32: lambda: _decode_float_array(src, rawdata, 4, "f"),
        DirectoryType.Float64: lambda: _decode_float_array(src, rawdata, 8, "d"),
        DirectoryType.URational: lambda: _decode_rational_array(src, rawdata, False),
        DirectoryType.Rational: lambda: _decode_rational_array(src, rawdata, True),
        DirectoryType.String: lambda: _extract_payload(src, rawdata, 1)[0:-1].decode("ascii"),
    }
    return switch_[src.Type]()
