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
    DNGQuality, LOCDistortion, LOCChromaticAberration, LOCDiffraction,
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


class _StandardSchema(object):
    def _decode(self, Schema, rawdata):
        container = Schema.parse(rawdata)
        for name, existence in container.FieldPresent.items():
            if name in self.__dict__:
                self.__dict__[name] = container[name] if existence else None
        return container


class CamDataGroup1(_StandardSchema):
    """DataGroup1 status information.

    Attributes:
        ShutterSpeed (int): Shutter speed (8-bit APEX step)
        Aperture (int): Aperture (8-bit APEX step)
        ProgramShift (sigma_ptpy.enum.ProgramShift): The dial operation amount in the camera side
            is not reflected.
        ISOAuto (sigma_ptpy.enum.ISOAuto): ISO auto
        ISOSpeed (int): ISO sensitivity (8-bit APEX step)
        ExpComp (int): Exposure compensation (8-bit APEX step). When the exposure mode is P, S,
            or A, the exposure compensation value is output. If it is M, a difference from the correct exposure
            of AE is output. If the exposure bracket is provided, the exposure compensation value is output,
            including the exposure bracket compensation value. (cf. "ExpCompExcludeAB" in DataGroup1)
        ABValue (int): Auto bracket value (8-bit APEX step)
        ABSetting (sigma_ptpy.enum.ABSetting): Auto bracket setting
        FrameBufferState (int): Free space of FrameBuffer (in camera) (Maximum number of shots)
        MediaFreeSpace (int): Free space of recording media (Maximum number of shots) (16bit)
        MediaStatus (int)
        CurrentLensFocalLength (float)
        BatteryState (int)
        ABShotRemainNumber (int): The remaining number of auto bracket shooting
        ExpCompExcludeAB (int)"""

    __FieldPresent = FlagsEnum(
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
        FrameBufferState=0x1)
    __Schema = Struct(
        '_Header' / Int8un,  # arbitrary value for parity
        'FieldPresent' / __FieldPresent,
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
        '_Parity' / Int8un)

    def __init__(self, ShutterSpeed=None, Aperture=None, ProgramShift=None, ISOAuto=None,
                 ISOSpeed=None, ExpComp=None, ABValue=None, ABSetting=None):
        self.ShutterSpeed = ShutterSpeed
        self.Aperture = Aperture
        self.ProgramShift = ProgramShift
        self.ISOAuto = ISOAuto
        self.ISOSpeed = ISOSpeed
        self.ExpComp = ExpComp
        self.ABValue = ABValue
        self.ABSetting = ABSetting
        self.CurrentLensFocalLength = None
        self.FrameBufferState = None
        self.MediaFreeSpace = None
        self.MediaStatus = None
        self.BatteryState = None
        self.ABShotRemainNumber = None
        self.ExpCompExcludeAB = None

    def __str__(self):
        return \
            f"CamDataGroup1(ShutterSpeed={str(self.ShutterSpeed)}, Aperture={str(self.Aperture)}, " \
            f"ProgramShift={str(self.ProgramShift)}, ISOAuto={str(self.ISOAuto)}, " \
            f"ISOSpeed={str(self.ISOSpeed)}, ExpComp={str(self.ExpComp)}, ABValue={str(self.ABValue)}, " \
            f"ABSetting={str(self.ABSetting)}, CurrentLensFocalLength={str(self.CurrentLensFocalLength)}, " \
            f"FrameBufferState={str(self.FrameBufferState)}, MediaFreeSpace={str(self.MediaFreeSpace)}, " \
            f"MediaStatus={str(self.MediaStatus)}, BatteryState={str(self.BatteryState)}," \
            f"ABShotRemainNumber={str(self.ABShotRemainNumber)}, ExpCompExcludeAB={str(self.ExpCompExcludeAB)})"

    def encode(self):
        return self.__Schema.build(Container(
            FieldPresent=Container(
                ShutterSpeed=self.ShutterSpeed is not None,
                Aperture=self.Aperture is not None,
                ProgramShift=self.ProgramShift is not None,
                ISOAuto=self.ISOAuto is not None,
                ISOSpeed=self.ISOSpeed is not None,
                ExpComp=self.ExpComp is not None,
                ABValue=self.ABValue is not None,
                ABSetting=self.ABSetting is not None,
                CurrentLensFocalLength=False, FrameBufferState=False, MediaFreeSpace=False, MediaStatus=False,
                BatteryState=False, ABShotRemainNumber=False, ExpCompExcludeAB=False, _Reserved0=False),
            _Header=0, _Parity=0,
            ShutterSpeed=self.ShutterSpeed, Aperture=self.Aperture, ProgramShift=self.ProgramShift,
            ISOAuto=self.ISOAuto, ISOSpeed=self.ISOSpeed, ExpComp=self.ExpComp,
            ABValue=self.ABValue, ABSetting=self.ABSetting, CurrentLensFocalLength=None,
            FrameBufferState=None, MediaFreeSpace=None, MediaStatus=None,
            BatteryState=None, ABShotRemainNumber=None, ExpCompExcludeAB=None, _Reserved0=None))

    def decode(self, rawdata):
        self._decode(self.__Schema, rawdata)


class CamDataGroup2(_StandardSchema):
    """DataGroup2 status information.

    Attributes:
        DriveMode (sigma_ptpy.enum.DriveMode): Drive mode
        SpecialMode (sigma_ptpy.enum.SpecialMode): Using LiveView or not
        ExposureMode (sigma_ptpy.enum.ExposureMode): P, A, S, or M
        AEMeteringMode (sigma_ptpy.enum.AEMeteringMode): Auto exposure setting
        FlashType (sigma_ptpy.enum.FlashType): Flash type (read-only)
        FlashMode (sigma_ptpy.enum.FlashMode): Flash mode
        FlashSeting (sigma_ptpy.enum.FlashSetting): Flash setting
        WhiteBalance (sigma_ptpy.enum.WhiteBalance): White balance
        Resolution (sigma_ptpy.enum.Resolution): Resolition
        ImageQuality (sigma_ptpy.enum.ImageQuality): JPEG or DNG"""
    __FieldPresent = FlagsEnum(
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
        FlashType=0x1)
    __Schema = Struct(
        '_Header' / Int8un,  # arbitrary value for parity
        'FieldPresent' / __FieldPresent,
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
        '_Parity' / Int8un)

    def __init__(self, DriveMode=None, SpecialMode=None, ExposureMode=None, AEMeteringMode=None,
                 FlashMode=None, FlashSetting=None, WhiteBalance=None,
                 Resolution=None, ImageQuality=None):
        self.DriveMode = DriveMode
        self.SpecialMode = SpecialMode
        self.ExposureMode = ExposureMode
        self.AEMeteringMode = AEMeteringMode
        self.FlashType = None
        self.FlashMode = FlashMode
        self.FlashSetting = FlashSetting
        self.WhiteBalance = WhiteBalance
        self.Resolution = Resolution
        self.ImageQuality = ImageQuality

    def __str__(self):
        return \
            f"CamDataGroup2(DriveMode={str(self.DriveMode)}, SpecialMode={str(self.SpecialMode)}, " \
            f"ExposureMode={str(self.ExposureMode)}, AEMeteringMode={str(self.AEMeteringMode)}, " \
            f"FlashType={str(self.FlashType)}, FlashMode={str(self.FlashMode)}, " \
            f"FlashSetting={str(self.FlashSetting)} WhiteBalance={str(self.WhiteBalance)}, " \
            f"Resolution={str(self.Resolution)}, ImageQuality={str(self.ImageQuality)})"

    def encode(self):
        return self.__Schema.build(Container(
            FieldPresent=Container(
                DriveMode=self.DriveMode is not None,
                SpecialMode=self.SpecialMode is not None,
                ExposureMode=self.ExposureMode is not None,
                AEMeteringMode=self.AEMeteringMode is not None,
                FlashMode=self.FlashMode is not None,
                FlashSetting=self.FlashSetting is not None,
                WhiteBalance=self.WhiteBalance is not None,
                Resolution=self.Resolution is not None,
                ImageQuality=self.ImageQuality is not None,
                FlashType=False, _Reserved0=False, _Reserved1=False, _Reserved2=False,
                _Reserved3=False, _Reserved4=False, _Reserved5=False),
            _Header=0, _Parity=0,
            DriveMode=self.DriveMode, SpecialMode=self.SpecialMode, ExposureMode=self.ExposureMode,
            AEMeteringMode=self.AEMeteringMode, FlashType=None, FlashMode=self.FlashMode,
            FlashSetting=self.FlashSetting, WhiteBalance=self.WhiteBalance, Resolution=self.Resolution,
            ImageQuality=self.ImageQuality, _Reserved0=None, _Reserved1=None, _Reserved2=None,
            _Reserved3=None, _Reserved4=None, _Reserved5=None))

    def decode(self, rawdata):
        self._decode(self.__Schema, rawdata)


class CamDataGroup3(_StandardSchema):
    """DataGroup3 status information.

    Attributes:
        ColorSpace (sigma_ptpy.enum.ColorSpace): sRGB or AdobeRGB
        ColorMode (sigma_ptpy.enum.ColorMode): Color mode
        BatteryKind (sigma_ptpy.enum.BatteryKind):
        LensWideFocalLength (float): focal length in mm (Wide end)
        LensTeleFocalLength (float): focal length in mm (Tele end)
        AFAuxLight (sigma_ptpy.enum.AFAuxLight): AF auxiliary light ON or OFF
        AFBeep (int): AF beep sound
        TimerSound (int): Timer sound
        DestToSave (sigma_ptpy.enum.DestToSave): Destination to save pictures"""
    __FieldPresent = FlagsEnum(
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
        AFAuxLight=0x1)
    __Schema = Struct(
        '_Header' / Int8un,  # arbitrary value for parity
        'FieldPresent' / __FieldPresent,
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
        '_Parity' / Int8un)

    def __init__(self, ColorSpace=None, ColorMode=None, AFAuxLight=None,
                 AFBeep=None, TimerSound=None, DestToSave=None):
        self.ColorSpace = ColorSpace
        self.ColorMode = ColorMode
        self.AFAuxLight = AFAuxLight
        self.AFBeep = AFBeep
        self.TimerSound = TimerSound
        self.DestToSave = DestToSave
        self.BatteryKind = None
        self.LensWideFocalLength = None
        self.LensTeleFocalLength = None

    def __str__(self):
        return \
            f"CamGroupData3(ColorSpace={str(self.ColorSpace)}, ColorMode={str(self.ColorMode)}, " \
            f"AFAuxLight={str(self.AFAuxLight)}, AFBeep={str(self.AFBeep)}, TimerSound={str(self.TimerSound)}, " \
            f"DestToSave={str(self.DestToSave)}, BatteryKind={str(self.BatteryKind)}, " \
            f"LensWideFocalLength={str(self.LensWideFocalLength)}, " \
            f"LensTeleFocalLength={str(self.LensTeleFocalLength)})"

    def encode(self):
        return self.__Schema.build(Container(
            FieldPresent=Container(
                ColorSpace=self.ColorSpace is not None,
                ColorMode=self.ColorMode is not None,
                AFAuxLight=self.AFAuxLight is not None,
                AFBeep=self.AFBeep is not None,
                TimerSound=self.TimerSound is not None,
                DestToSave=self.DestToSave is not None,
                BatteryKind=False, LensWideFocalLength=False, LensTeleFocalLength=False, _Reserved0=False,
                _Reserved1=False, _Reserved2=False, _Reserved3=False, _Reserved4=False, _Reserved5=False,
                _Reserved6=False),
            _Header=0, _Parity=0,
            ColorSpace=self.ColorSpace, ColorMode=self.ColorMode, AFAuxLight=self.AFAuxLight,
            AFBeep=self.AFBeep, TimerSound=self.TimerSound, DestToSave=self.DestToSave,
            BatteryKind=None, LensWideFocalLength=None, LensTeleFocalLength=None, _Reserved0=None,
            _Reserved1=None, _Reserved2=None, _Reserved3=None, _Reserved4=None, _Reserved5=None, _Reserved6=None))

    def decode(self, rawdata):
        self._decode(self.__Schema, rawdata)


class CamDataGroup4(_StandardSchema):
    """DataGroup4 status information.

    Attributes:
        DCCropMode (sigma_ptpy.enum.DCCropMode): The DC Crop setting value and AUTO are judged
            depending on the attached lens.
        LVMagnifyRatio (sigma_ptpy.enum.LVMagnifyRatio`)
        HighISOExt (sigma_ptpy.enum.HighISOExt`): Setting value of high-sensitivity ISO extension
        ContShootSpeed (sigma_ptpy.enum.ContShootSpeed): Setting value of continuous shooting speed
        HDR (sigma_ptpy.enum.HDR):
        DNGQuality (sigma_ptpy.enum.DNGQuality): DNG image quality
        FillLight (sigma_ptpy.enum.FillLight): Setting value of Fill Light. Set the ±5.0 range
            in 0.1 increments, and enter 10 times the UI display value.
        LOCDistortion (sigma_ptpy.enum.LOCDistortion):
            Lens Optics Compensation - Distortion setting value
        LOCChromaticAberration (sigma_ptpy.enum.LOCChromaticAberration):
            Lens Optics Compensation - Chromatic Aberration setting value
        LOCDiffraction (sigma_ptpy.enum.LOCDiffraction):
            Lens Optics Compensation - Diffraction setting value
        LOCVignetting (sigma_ptpy.enum.LOCVignetting):
            Lens Optics Compensation - Vignetting setting value
        LOCColorShade (sigma_ptpy.enum.LOCColorShade):
            Lens Optics Compensation - Color Shading setting value
        LOCColorShadeAcq (sigma_ptpy.enum.LOCColorShadeAcq):
            Lens Optics Compensation - Color Shading compensation value acquirement.
            Leave it ON from the time you entered the compensation value capture menu using
            camera or application operation until the time you exit the menu.
        EImageStab (sigma_ptpy.enum.EImageStab): Setting value of Electronic Image Stabilization
        ShutterSound (sigma_ptpy.enum.ShutterSound): Shutter sound / Recording start/stop sound"""
    __FieldPresent = FlagsEnum(
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
        HDR=0x1)
    __Schema = Struct(
        '_Header' / Int8un,  # arbitrary value for parity
        'FieldPresent' / __FieldPresent,
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
        'LOCChromaticAberration' / _IfDefined('LOC', _Enum(Int8un, LOCChromaticAberration)),
        'LOCDiffraction' / _IfDefined('LOC', _Enum(Int8un, LOCDiffraction)),
        'LOCVignetting' / _IfDefined('LOC', _Enum(Int8un, LOCVignetting)),
        'LOCColorShade' / _IfDefined('LOC', _Enum(Int8un, LOCColorShade)),
        'LOCColorShadeAcq' / _IfDefined('LOC', _Enum(Int8un, LOCColorShadeAcq)),
        'EImageStab' / _IfDefined('EImageStab', _Enum(Int8un, EImageStab)),
        'ShutterSound' / _IfDefined('ShutterSound', Int8un),
        '_Reserved4' / _IfDefined('_Reserved4', Int8un),
        '_Reserved5' / _IfDefined('_Reserved5', Int8un),
        '_Parity' / Int8un)

    def __init__(self, DCCropMode=None, LVMagnifyRatio=None, HighISOExt=None,
                 ContShootSpeed=None, HDR=None, DNGQuality=None, FillLight=None,
                 LOCDistortion=None, LOCChromaticAberration=None, LOCDiffraction=None,
                 LOCVignetting=None, LOCColorShade=None, LOCColorShadeAcq=None,
                 EImageStab=None, ShutterSound=None):
        self.DCCropMode = DCCropMode
        self.LVMagnifyRatio = LVMagnifyRatio
        self.HighISOExt = HighISOExt
        self.ContShootSpeed = ContShootSpeed
        self.HDR = HDR
        self.DNGQuality = DNGQuality
        self.FillLight = FillLight
        self.LOCDistortion = LOCDistortion
        self.LOCChromaticAberration = LOCChromaticAberration
        self.LOCDiffraction = LOCDiffraction
        self.LOCVignetting = LOCVignetting
        self.LOCColorShade = LOCColorShade
        self.LOCColorShadeAcq = LOCColorShadeAcq
        self.EImageStab = EImageStab
        self.ShutterSound = ShutterSound

    def __str__(self):
        return \
            f"CamDataGroup4(DCCropMode={str(self.DCCropMode)}, LVMagnifyRatio={str(self.LVMagnifyRatio)}, " \
            f"HighISOExt={str(self.HighISOExt)}, ContShootSpeed={str(self.ContShootSpeed)}, " \
            f"HDR={str(self.HDR)}, DNGQuality={str(self.DNGQuality)}, FillLight={str(self.FillLight)}, " \
            f"LOCDistortion={str(self.LOCDistortion)}, LOCChromaticAberration={str(self.LOCChromaticAberration)}, " \
            f"LOCDiffraction={str(self.LOCDiffraction)}, LOCVignetting={str(self.LOCVignetting)}, " \
            f"LOCColorShade={str(self.LOCColorShade)}, LOCColorShadeAcq={str(self.LOCColorShadeAcq)}, " \
            f"EImageStab={str(self.EImageStab)}, ShutterSound={str(self.ShutterSound)})"

    def encode(self):
        LOC = LOCDistortion is not None or LOCChromaticAberration is not None or LOCDiffraction is not None \
            or LOCVignetting is not None or LOCColorShade is not None or LOCColorShadeAcq is not None
        return self.__Schema.build(Container(
            FieldPresent=Container(
                DCCropMode=(self.DCCropMode is not None),
                LVMagnifyRatio=(self.LVMagnifyRatio is not None),
                HighISOExt=(self.HighISOExt is not None),
                ContShootSpeed=(self.ContShootSpeed is not None),
                HDR=(self.HDR is not None),
                DNGQuality=(self.DNGQuality is not None),
                FillLight=(self.FillLight is not None),
                EImageStab=(self.EImageStab is not None),
                ShutterSound=(self.ShutterSound is not None),
                LOC=LOC, _Reserved0=False, _Reserved1=False, _Reserved2=False,
                _Reserved3=False, _Reserved4=False, _Reserved5=False),
            _Header=0, _Parity=0,
            DCCropMode=self.DCCropMode, LVMagnifyRatio=self.LVMagnifyRatio, HighISOExt=self.HighISOExt,
            ContShootSpeed=self.ContShootSpeed, HDR=self.HDR, DNGQuality=self.DNGQuality,
            FillLight=self.FillLight, EImageStab=self.EImageStab, ShutterSound=self.ShutterSound,
            LOCDistortion=self.LOCDistortion or 0, LOCChromaticAberration=self.LOCChromaticAberration or 0,
            LOCDiffraction=self.LOCDiffraction or 0, LOCVignetting=self.LOCVignetting or 0,
            LOCColorShade=self.LOCColorShade or 0, LOCColorShadeAcq=self.LOCColorShadeAcq or 0,
            _Reserved0=None, _Reserved1=None, _Reserved2=None, _Reserved3=None, _Reserved4=None, _Reserved5=None))

    def decode(self, rawdata):
        container = self._decode(self.__Schema, rawdata)
        if container.FieldPresent.LOC:
            self.LOCDistortion = container.LOCDistortion
            self.LOCChromaticAberration = container.LOCChromaticAberration
            self.LOCDiffraction = container.LOCDiffraction
            self.LOCVignetting = container.LOCVignetting
            self.LOCColorShade = container.LOCColorShade
            self.LOCColorShadeAcq = container.LOCColorShadeAcq


class CamDataGroup5(_StandardSchema):
    """DataGroup5 status information.

    Attributes:
        IntervalTimerSecond (int): Shooting interval in Interval Timer mode (Unit in seconds).
        IntervalTimerFrame (int): The number of shots in Interval Timer mode.
            0 indicates the infinite, and other numeric values indicate the specified number of shots.
        IntervalTimerSecondRemain (int): Remaining time required to start the next
            shooting in Interval Timer mode (Unit in seconds).
        IntervalTimerFrameRemain (int): Remaining time required to end shooting in Interval Timer mode.
        ColorTemp (int): User setting value of color temperature white balance (Unit in kelvin).
        AspectRatio (sigma_ptpy.enum.AspectRatio): Aspect Ratio setting value.
        ToneEffect (sigma_ptpy.enum.ToneEffect): Tone setting value in Monochrome mode.
        AFAuxLightEF (sigma_ptpy.enum.AFAuxLightEF): Auxiliary light activation setting for external flash."""
    __FieldPresent = FlagsEnum(
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
        _Reserved4=0x1)
    __Schema = Struct(
        '_Header' / Int8un,  # arbitrary value for parity
        'FieldPresent' / __FieldPresent,
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
        '_Parity' / Int8un)

    def __init__(self, IntervalTimerSecond=None, IntervalTimerFrame=None,
                 ColorTemp=None, AspectRatio=None, ToneEffect=None, AFAuxLightEF=None):
        self.IntervalTimerSecond = IntervalTimerSecond
        self.IntervalTimerFrame = IntervalTimerFrame
        self.IntervalTimerSecondRemain = None
        self.IntervalTimerFrameRemain = None
        self.ColorTemp = ColorTemp
        self.AspectRatio = AspectRatio
        self.ToneEffect = ToneEffect
        self.AFAuxLightEF = AFAuxLightEF

    def __str__(self):
        return \
            f"CamDataGroup5(IntervalTimerSecond={str(self.IntervalTimerSecond)}, " \
            f"IntervalTimerFrame={str(self.IntervalTimerFrame)}, " \
            f"IntervalTimerSecondRemain={str(self.IntervalTimerSecondRemain)}, " \
            f"IntervalTimerFrameRemain={str(self.IntervalTimerFrameRemain)}, " \
            f"ColorTemp={str(self.ColorTemp)}, AspectRatio={str(self.AspectRatio)}, " \
            f"ToneEffect={str(self.ToneEffect)}, AFAuxLightEF={str(self.AFAuxLightEF)})"

    def encode(self):
        if (self.IntervalTimerSecond is not None) != (self.IntervalTimerFrame is not None):
            raise ValueError("Both of IntervalTimerSecond and IntervalTimerFrame must be specified.")
        return self.__Schema.build(Container(
            FieldPresent=Container(
                IntervalTimer=self.IntervalTimerSecond is not None,
                ColorTemp=self.ColorTemp is not None,
                AspectRatio=self.AspectRatio is not None,
                ToneEffect=self.ToneEffect is not None,
                AFAuxLightEF=self.AFAuxLightEF is not None,
                IntervalTimerSecondRemain=False, IntervalTimerFrameRemain=False,
                _Reserved0=False, _Reserved1=False, _Reserved2=False, _Reserved3=False,
                _Reserved4=False, _Reserved5=False, _Reserved6=False, _Reserved7=False,
                _Reserved8=False, _Reserved9=False, _Reserved10=False),
            _Header=0, _Parity=0,
            IntervalTimerSecond=self.IntervalTimerSecond, IntervalTimerFrame=self.IntervalTimerFrame,
            ColorTemp=self.ColorTemp, AspectRatio=self.AspectRatio, ToneEffect=self.ToneEffect,
            AFAuxLightEF=self.AFAuxLightEF, IntervalTimerSecondRemain=0,
            IntervalTimerFrameRemain=0, _Reserved0=None, _Reserved1=None, _Reserved2=None, _Reserved3=None,
            _Reserved4=None, _Reserved5=None, _Reserved6=None, _Reserved7=None, _Reserved8=None,
            _Reserved9=None, _Reserved10=None))

    def decode(self, rawdata):
        container = self._decode(self.__Schema, rawdata)
        if container.FieldPresent.IntervalTimer:
            self.IntervalTimerSecond = container.IntervalTimerSecond
            self.IntervalTimerFrame = container.IntervalTimerFrame
            self.IntervalTimerSecondRemain = container.IntervalTimerSecondRemain
            self.IntervalTimerFrameRemain = container.IntervalTimerFrameRemain


class CamCaptStatus(object):
    __Schema = Struct(
        '_Header' / Int8un,  # arbitrary value for parity
        'ImageId' / Int8un,
        'ImageDBHead' / Int8un,
        'ImageDBTail' / Int8un,
        'CaptStatus' / _Enum(Int16ul, CaptStatus),
        'DestToSave' / _Enum(Int8un, DestToSave),
        '_Parity' / Int8un)

    def __init__(self):
        self.ImageId = None
        self.ImageDBHead = None
        self.ImageDBTail = None
        self.CaptStatus = None
        self.DestToSave = None

    def __str__(self):
        return \
            f"CamCaptStatus(ImageId={str(self.ImageId)}, ImageDBHead={str(self.ImageDBHead)}, " \
            f"ImageDBTail={str(self.ImageDBTail)}, CaptStatus={str(self.CaptStatus)}, " \
            f"DestToSave={str(self.DestToSave)})"

    def decode(self, rawdata):
        container = self.__Schema.parse(rawdata)
        self.ImageId = container.ImageId
        self.ImageDBHead = container.ImageDBHead
        self.ImageDBTail = container.ImageDBTail
        self.CaptStatus = container.CaptStatus
        self.DestToSave = container.DestToSave


class SnapCommand(object):
    __Schema = Struct(
        '_Header' / Int8un,  # arbitrary value for parity
        'CaptureMode' / _Enum(Int8un, CaptureMode),
        'CaptureAmount' / Int8un,
        '_Parity' / Int8un)

    def __init__(self, CaptureMode=CaptureMode.GeneralCapt, CaptureAmount=1):
        self.CaptureMode = CaptureMode
        self.CaptureAmount = CaptureAmount

    def encode(self):
        return self.__Schema.build(Container(
            _Header=0, _Parity=0,
            CaptureMode=self.CaptureMode, CaptureAmount=self.CaptureAmount))


class PictFileInfo2(object):
    __Schema = Struct(
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
        '_Unknown1' / Bytes(2))  # ?

    def __str__(self):
        return \
            f"PictFileInfo2(FileAddress={str(self.FileAddress)}, FileSize={str(self.FileSize)}, " \
            f"PictureFormat={str(self.PictureFormat)}, SizeX={str(self.SizeX)}, SizeY={str(self.SizeY)}, " \
            f"PathName={str(self.PathName)}, FileName={str(self.FileName)})"

    def decode(self, rawdata):
        container = self.__Schema.parse(rawdata)
        self.FileAddress = container.FileAddress
        self.FileSize = container.FileSize
        self.PictureFormat = container.PictureFormat
        self.SizeX = container.SizeX
        self.SizeY = container.SizeY
        self.PathName = container.PathName
        self.FileName = container.FileName


class BigPartialPictFile(object):
    """A partial byte array of a picture file in a camera.

    Attributes:
        AcquiredSize (int): the number of bytes in PartialData.
        PartialData (bytes): partial data of a picture file (JPEG encoded)."""
    __Schema = Struct(
        'AcquiredSize' / Int32ul,
        'PartialData' / GreedyBytes)

    def decode(self, rawdata):
        container = self.__Schema.parse(rawdata)
        self.AcquiredSize = container.AcquiredSize
        self.PartialData = container.PartialData


class ViewFrame(object):
    """A live view frame in a camera.

    Attributes:
        Data (bytes): data of a picture (JPEG encoded)."""
    __Schema = Struct(
        '_Unknown0' / Bytes(10),  # ?
        'Data' / GreedyBytes)

    def decode(self, rawdata):
        container = self.__Schema.parse(rawdata)
        self.Data = container.Data


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


def _map_list(f):
    def g(lst):
        return [f(x) for x in lst]
    return g


def _bool(x):
    return x == [1]


class CamCanSetInfo5(_DirectoryEntrySchema):
    def __str__(self):
        s = ", ".join([f"{k}={str(v)}" for k, v in self.__dict__.items()])
        return f"CamCanSetInfo5({s})"

    def decode(self, rawdata):
        field_defs = [
            (1, "DriveMode", _map_list(lambda x: DriveMode.IntervalTimer if x == 5 else DriveMode(x))),
            (2, "ContShootSpeed", _map_list(ContShootSpeed)),
            (3, "IntervalTimerFrame", lambda x: {"InfiniteSetting": x[0] == 1, "FiniteSetting": x[1] == 1}),
            (4, "IntervalTimerSecond", None),
            (10, "SFD", None),
            (11, "ImageQuality", {
                "2": ImageQuality.DNG,
                "16": ImageQuality.JPEGFine,
                "32": ImageQuality.JPEGNormal,
                "48": ImageQuality.JPEGBasic,
                "18": ImageQuality.DNGAndJPEG,
            }),
            (12, "DNGQuality", _map_list(DNGQuality)),
            (20, "StillImageResolution", {
                "1": Resolution.High,
                "2": Resolution.Medium,
                "3": Resolution.Low,
            }),
            (21, "AspectRatio", _map_list(AspectRatio)),
            (100, "StillMovieSwitch", None),
            (110, "AudioRecord", None),
            (111, "NumOfVoiceChannels", None),
            (112, "GainAdjustMethod", None),
            (113, "ManualGainAdjustEV", None),
            (114, "WindNoiseCanceller", None),
            (150, "RecordFormat", None),
            (151, "CinemaDNGImageQuality", None),
            (152, "MovImageQuality", None),
            (160, "MovieResolution", None),
            (161, "FrameRate", None),
            (162, "Binning", None),
            (200, "ExposureMode", {
                "1": ExposureMode.ProgramAuto,
                "2": ExposureMode.AperturePriority,
                "3": ExposureMode.ShutterPriority,
                "4": ExposureMode.Manual,
                "5": ExposureMode.C1,
                "6": ExposureMode.C2,
                "7": ExposureMode.C3,
            }),
            (201, "ProgramShiftAvailable", _bool),
            (210, "FValue", None),
            (211, "TValue", None),
            (212, "ShutterSpeed", None),
            (213, "NonApexShutterSpeed", None),
            (214, "ShutterAngle", None),
            (215, "ISOManual", None),
            (216, "ISOAuto", None),
            (217, "ExpComp", None),
            (218, "ExpBracketNum", None),
            (219, "ExpBracketOrder", None),
            (220, "ExpBracketAmount", None),
            (250, "AEMeteringMode", {
                "1": AEMeteringMode.Evaluative,
                "2": AEMeteringMode.CenterWeightedAverage,
                "3": AEMeteringMode.Spot,
            }),
            (251, "AELockAvailable", _bool),
            (252, "Flash", None),
            (253, "FlashExpComp", None),
            (300, "CustomBracket", None),
            (301, "WhiteBalance", {
                "1": WhiteBalance.Auto,
                "2": WhiteBalance.LightSource,
                "3": WhiteBalance.Sunlight,
                "4": WhiteBalance.Shade,
                "5": WhiteBalance.Incandescent,
                "6": WhiteBalance.Fluorescent,
                "7": WhiteBalance.Flash,
                "8": WhiteBalance.ColorTemp,
                "9": WhiteBalance.Custom1,
                "10": WhiteBalance.Custom2,
                "11": WhiteBalance.Custom3,
            }),
            (302, "WBColorTemp", None),
            (303, "WBCustomCap", None),
            (304, "WBAdjustment", None),
            (305, "WBBracketNum", None),
            (306, "WBBracketDirection", None),
            (307, "WBBracketEV", None),
            (320, "ColorMode", {
                "1": ColorMode.Normal,
                "2": ColorMode.Vivid,
                "3": ColorMode.Neutral,
                "4": ColorMode.Portrait,
                "5": ColorMode.Landscape,
                "6": ColorMode.Cinema,
                "7": ColorMode.Sunset,
                "8": ColorMode.Forest,
                "9": ColorMode.FovClassicBlue,
                "10": ColorMode.FovClassicYellow,
                "11": ColorMode.Monochrome,
            }),
            (321, "ColorModeContrast", None),
            (322, "ColorModeSharpness", None),
            (323, "ColorModeSaturation", None),
            (323, "MonochromeFilterEffect", None),
            (324, "MonochromeToneEffect", None),
            (327, "ColorModeBracketNum", None),
            (340, "FillLight", None),
            (341, "FillLightBracketNum", None),
            (342, "FillLightBracketEV", None),
            (350, "HDR", {
                "-1": HDR.Auto,
                "0": HDR.Off,
                "1": HDR.PlusMinus1,
                "2": HDR.PlusMinus2,
                "3": HDR.PlusMinus3,
            }),
            (500, "DCCropMode", {
                "-1": DCCropMode.Auto,
                "0": DCCropMode.Off,
                "1": DCCropMode.On,
            }),
            (501, "LOCDistortion", {"-1": LOCDistortion.Auto, "0": LOCDistortion.Off}),
            (502, "LOCChromaticAberration", {"-1": LOCChromaticAberration.Auto, "0": LOCChromaticAberration.Off}),
            (503, "LOCDiffraction", {"0": LOCDiffraction.Off, "1": LOCDiffraction.On}),
            (504, "LOCVignetting", {"-1": LOCVignetting.Auto, "0": LOCVignetting.Off}),
            (505, "LOCColorShade", {
                "-1": LOCColorShade.Auto,
                "0": LOCColorShade.Off,
                "1": LOCColorShade.No1,
                "2": LOCColorShade.No2,
                "3": LOCColorShade.No3,
                "4": LOCColorShade.No4,
                "5": LOCColorShade.No5,
                "6": LOCColorShade.No6,
                "7": LOCColorShade.No7,
                "8": LOCColorShade.No8,
                "9": LOCColorShade.No9,
                "10": LOCColorShade.No10,
            }),
            (506, "LOCColorShadeCustomCapAvailable", _bool),
            (600, "FocusMode", _map_list(FocusMode)),
            (601, "AFLockAvailable", _bool),
            (602, "FaceEyeAF", _map_list(FaceEyeAF)),
            (610, "FocusArea", _map_list(FocusArea)),
            (611, "OnePointSelection", _map_list(OnePointSelection)),
            (612, "FocusAreaOverallArea", lambda x: {'Height': x[0], 'Width': x[1]}),
            (613, "FocusAreaValidArea", lambda x: {'Top': x[0], 'Bottom': x[1], 'Left': x[2], 'Right': x[3]}),
            (614, "NumOfDMFSizes", lambda x: x[0]),
            (615, "DMFSize", lambda x: [(x[i], x[i + 1]) for i in range(0, len(x), 2)]),
            (616, "DMFMovement", None),
            (650, "PreConstAF", _map_list(PreConstAF)),
            (651, "FocusLimit", _map_list(FocusLimit)),
            (656, "AFSOperation", None),
            (657, "AFCOperation", None),
            (700, "LVImageTransferAvailable", _bool),
            (701, "LVMagnificationRate", None),
            (702, "FocusPeaking", None),
            (800, "DateTime", None),
            (801, "ShutterSound", None),
            (802, "AFVolume", None),
            (803, "TimerVolume", None),
            (810, "EImageStab", {"0": EImageStab.Off, "1": EImageStab.On}),
        ]
        response = dict((str(tag), val) for tag, val in self._decode(rawdata))
        for tag, name, conv in field_defs:
            tag = str(tag)
            if tag in response:
                val = response[tag]
                if type(conv) is dict:
                    self.__dict__[name] = [conv[str(v)] if str(v) in conv else v for v in val]
                elif conv is not None:
                    self.__dict__[name] = conv(val)
                else:
                    self.__dict__[name] = val
            else:
                self.__dict__[name] = None
