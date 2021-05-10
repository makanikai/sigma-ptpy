"""Schema definitions for the SIGMA fp series"""

import struct
from construct import (
    Adapter, Bytes, Container, FlagsEnum,
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
    AspectRatio, ToneEffect, AFAuxLightEF,
    FocusMode, AFLock, FaceEyeAF, FaceEyeAFStatus, FocusArea,
    OnePointSelection, PreConstAF, FocusLimit
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


def _decode_int_array(b, size, signed):
    return [int.from_bytes(b[i:i + size], byteorder="little", signed=signed) for i in range(0, len(b), size)]


def _decode_float_array(b, size, fmt):
    count = int(len(b) / size)
    return list(struct.unpack("<" + fmt * count, b))


def _decode_rational_array(b, signed):
    return [(int.from_bytes(b[i:i + 4], byteorder="little", signed=signed),
             int.from_bytes(b[i + 4:i + 8], byteorder="little", signed=signed)) for i in range(0, len(b), 8)]


def _encode_rational(v, signed=None):
    return \
        v[0].to_bytes(4, byteorder="little", signed=signed) \
        + v[1].to_bytes(4, byteorder="little", signed=signed)


_sizes = {
    DirectoryType.UInt8: 1,
    DirectoryType.Any8: 1,
    DirectoryType.Int8: 1,
    DirectoryType.UInt16: 2,
    DirectoryType.Int16: 2,
    DirectoryType.UInt32: 4,
    DirectoryType.Int32: 4,
    DirectoryType.Float32: 4,
    DirectoryType.Float64: 8,
    DirectoryType.URational: 8,
    DirectoryType.Rational: 8,
    DirectoryType.String: 1,
}

_decoders = {
    DirectoryType.UInt8: lambda b: _decode_int_array(b, 1, False),
    DirectoryType.Any8: lambda b: _decode_int_array(b, 1, False),
    DirectoryType.Int8: lambda b: _decode_int_array(b, 1, True),
    DirectoryType.UInt16: lambda b: _decode_int_array(b, 2, False),
    DirectoryType.Int16: lambda b: _decode_int_array(b, 2, True),
    DirectoryType.UInt32: lambda b: _decode_int_array(b, 4, False),
    DirectoryType.Int32: lambda b: _decode_int_array(b, 4, True),
    DirectoryType.Float32: lambda b: _decode_float_array(b, 4, "f"),
    DirectoryType.Float64: lambda b: _decode_float_array(b, 8, "d"),
    DirectoryType.URational: lambda b: _decode_rational_array(b, False),
    DirectoryType.Rational: lambda b: _decode_rational_array(b, True),
    DirectoryType.String: lambda b: b[0:-1].decode("ascii"),
}

_encoders = {
    DirectoryType.UInt8: lambda v: v.to_bytes(1, byteorder="little", signed=False),
    DirectoryType.Any8: lambda v: v.to_bytes(1, byteorder="little", signed=False),
    DirectoryType.Int8: lambda v: v.to_bytes(1, byteorder="little", signed=True),
    DirectoryType.UInt16: lambda v: v.to_bytes(2, byteorder="little", signed=False),
    DirectoryType.Int16: lambda v: v.to_bytes(2, byteorder="little", signed=True),
    DirectoryType.UInt32: lambda v: v.to_bytes(4, byteorder="little", signed=False),
    DirectoryType.Int32: lambda v: v.to_bytes(4, byteorder="little", signed=True),
    DirectoryType.Float32: lambda v: struct.pack("<f", v),
    DirectoryType.Float64: lambda v: struct.pack("<d", v),
    DirectoryType.URational: lambda v: _encode_rational(v, signed=False),
    DirectoryType.Rational: lambda v: _encode_rational(v, signed=True),
    DirectoryType.String: lambda v: v.encode("ascii") + b"\x00"
}

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


class _DirectoryEntrySchema(object):
    def _decode(self, rawdata):
        dirarray = _DirectoryEntryArray.parse(rawdata)
        real_directory_count = min(len(dirarray.Entries), dirarray.DirectoryCount)

        pairs = list()
        for entry in dirarray.Entries[0:real_directory_count]:
            size = _sizes[entry.Type]
            n = entry.Count * size
            if n <= 4:
                payload = entry.Value[0:n]
            else:
                i = int.from_bytes(entry.Value, byteorder="little", signed=False)
                payload = rawdata[i:i + n]

            val = _decoders[entry.Type](payload)
            pairs.append((entry.Tag, val))

        return pairs

    def _encode(self, triples):
        header_size = 8
        index_section_size = header_size + len(triples) * _DirectoryEntry.sizeof()
        index_section = []
        data_section = b""

        for tag, type_, val in triples:
            # Converts a tag from EnumClass to int
            if type(tag) is not int:
                tag = tag.value
            # Converts a value into bytes
            if type(val) is list:
                count = len(val)
                payload = b"".join(map(_encoders[type_], val))
            elif type(val) is str:
                payload = _encoders[type_](val)
                count = len(payload)
            else:
                count = 1
                payload = _encoders[type_](val)
            # Adds a padding for 4-byte alignment
            if len(payload) % 4 != 0:
                payload += b"\x00" * (4 - len(payload) % 4)
            # Appends a new index into index_section
            if len(payload) <= 4:
                index_section.append(Container(Tag=tag, Type=type_.value, Count=count, Value=payload))
            else:
                offset = (index_section_size + len(data_section)).to_bytes(4, byteorder="little", signed=False)
                data_section += payload
                index_section.append(Container(Tag=tag, Type=type_.value, Count=count, Value=offset))

        array = Container(
            DataLength=index_section_size + len(data_section),
            DirectoryCount=len(index_section),
            Entries=index_section,
        )
        return _DirectoryEntryArray.build(array) + data_section


class ApiConfig(_DirectoryEntrySchema):
    """SIGMA API information.

    Attributes:
        CameraModel (str): The model name of a camera (read-only).
        SerialNumber (str): The serial number of a camera (read-only).
        FirmwareVersion (str): The firmware version of a camera (read-only).
        CommunicationVersion (float): The communication version of a camera (read-only)."""

    def __init__(self):
        self.CameraModel = None
        self.SerialNumber = None
        self.FirmwareVersion = None
        self.CommunicationVersion = None

    def __str__(self):
        return \
            f"ApiConfig(CameraModel={str(self.CameraModel)}, SerialNumber={str(self.SerialNumber)}, " \
            f"FirmwareVersion={str(self.FirmwareVersion)}, CommunicationVersion={str(self.CommunicationVersion)})"

    def decode(self, rawdata):
        for tag, val in self._decode(rawdata):
            if tag == 1:
                self.CameraModel = val
            elif tag == 2:
                self.SerialNumber = val
            elif tag == 3:
                self.FirmwareVersion = val
            elif tag == 5:
                self.CommunicationVersion = val[0]


class CamDataGroupFocus(_DirectoryEntrySchema):
    """Focus-related information.

    Attributes:
        FocusMode (sigma_ptpy.enum.FocusMode): Setting value of Focus mode.
        AFLock (sigma_ptpy.enum.AFLock): AF is locked, or not.
        FaceEyeAF (sigma_ptpy.enum.FaceEyeAF): Setting value of Face / Eye Priority AF.
        FaceEyeAFStatus (sigma_ptpy.enum.FaceEyeAFStatus): Face / Eye detection status (read-only).
        FocusArea (sigma_ptpy.enum.FocusArea): Setting value of focus area.
        OnePointSelection (sigma_ptpy.enum.OnePointSelection): Setting value when the focus area is set to 1-point selection.
        DMFSize (int): Size setting of distance measurement frame.
        DMFPos (list): Record the user setting value of the distance measurement frame in the array format in
            the following order. Vertical and horizontal coordinates of gravity. The frame size is determined
            for each mode, therefore, set only the position according to the position of the CanSetInfo5v
            focus area coordinate system.
        DMFDetection (list): Face detection frame or distance measurement frame information used for focus
            judgment (read-only). For one distance measurement frame, record items in the array format in the
            following order.
            Vertical and horizontal coordinates of gravity, vertical width, horizontal width. If there are
            multiple distance measurement frames, connect and arrange items by the number of frames in the
            format above.
        PreConstAF (sigma_ptpy.enum.PreConstAF): For a still image, specify the Pre-AF setting value.
            For a movie, specify the Constant AF setting value.
        FocusLimit (sigma_ptpy.enum.FocusLimit): Focus limit setting value."""

    def __init__(self, FocusMode=None, AFLock=None, FaceEyeAF=None, FocusArea=None,
                 OnePointSelection=None, DMFSize=None, DMFPos=None,
                 PreConstAF=None, FocusLimit=None):
        self.FocusMode = FocusMode
        self.AFLock = AFLock
        self.FaceEyeAF = FaceEyeAF
        self.FaceEyeAFStatus = None
        self.FocusArea = FocusArea
        self.OnePointSelection = OnePointSelection
        self.DMFSize = DMFSize
        self.DMFPos = DMFPos
        self.DMFDetection = None
        self.PreConstAF = PreConstAF
        self.FocusLimit = FocusLimit

    def __str__(self):
        return \
            f"CamDataGroupFocus(FocusMode={str(self.FocusMode)}, AFLock={str(self.AFLock)}, " \
            f"FaceEyeAF={str(self.FaceEyeAF)}, FaceEyeAFStatus={str(self.FaceEyeAFStatus)}, " \
            f"FocusArea={str(self.FocusArea)}, OnePointSelection={str(self.OnePointSelection)}, " \
            f"DMFSize={str(self.DMFSize)}, DMFPos={str(self.DMFPos)}, " \
            f"DMFDetection={str(self.DMFDetection)}, PreConstAF={str(self.PreConstAF)}, " \
            f"FocusLimit={str(self.FocusLimit)})"

    def encode(self):
        data = list()

        if self.FocusMode is not None:
            data.append((1, DirectoryType.UInt8, self.FocusMode.value))
        if self.AFLock is not None:
            data.append((2, DirectoryType.UInt8, self.AFLock.value))
        if self.FaceEyeAF is not None:
            data.append((3, DirectoryType.UInt8, self.FaceEyeAF.value))
        if self.FocusArea is not None:
            data.append((10, DirectoryType.UInt8, self.FaceEyFocusAreaeAF.value))
        if self.FocusArea is not None:
            data.append((10, DirectoryType.UInt8, self.FocusArea.value))
        if self.OnePointSelection is not None:
            data.append((11, DirectoryType.UInt8, self.OnePointSelection.value))
        if self.DMFSize is not None:
            data.append((12, DirectoryType.UInt8, self.DMFSize.value))
        if self.DMFPos is not None:
            data.append((13, DirectoryType.UInt8, self.DMFPos.value))
        if self.PreConstAF is not None:
            data.append((51, DirectoryType.UInt8, self.PreConstAF.value))
        if self.FocusLimit is not None:
            data.append((52, DirectoryType.UInt8, self.FocusLimit.value))

        return self._encode(data)

    def decode(self, rawdata):
        for tag, val in self._decode(rawdata):
            if tag == 1:
                self.FocusMode = FocusMode(val[0])
            elif tag == 2:
                self.AFLock = AFLock(val[0])
            elif tag == 3:
                self.FaceEyeAF = FaceEyeAF(val[0])
            elif tag == 4:
                self.FaceEyeAFStatus = FaceEyeAFStatus(val[0])
            elif tag == 10:
                self.FocusArea = FocusArea(val[0])
            elif tag == 11:
                self.OnePointSelection = OnePointSelection(val[0])
            elif tag == 12:
                self.DMFSize = val[0]
            elif tag == 13:
                self.DMFPos = val
            elif tag == 14:
                self.DMFDetection = val
            elif tag == 51:
                self.PreConstAF = PreConstAF(val[0])
            elif tag == 52:
                self.FocusLimit = FocusLimit(val[0])
