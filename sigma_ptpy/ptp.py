import logging
from ptpy import PTP
from construct import (
    Array, BitsInteger, Bitwise, Container, Default, Enum, Int16sb,
    Int16sl, Int16sn, Int16ub, Int16ul, Int16un, Int32sb, Int32sl, Int32sn,
    Int32ub, Int32ul, Int32un, Int64sb, Int64sl, Int64sn, Int64ub, Int64ul,
    Int64un, Int8sb, Int8sl, Int8sn, Int8ub, Int8ul, Int8un, Pass, Padding,
    PrefixedArray, Struct, Switch, If
)

logger = logging.getLogger(__name__)

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
    _DriveMode = Enum(
        Int8un,
        default=Pass,
        Uninitialized=0,
        SingleCapture=1,
        ContinuousCapture=2,
        TwoSecondsSelfTimer=3,
        TenSecondsSelfTimer=4,
        IntervalTimer=7
    )
    _SpecialMode = Enum(
        Int8un,
        default=Pass,
        Uninitialized=0x00,
        LiveViewMode=0x02
    )
    _ExposureMode = Enum(
        Int8un,
        default=Pass,
        Uninitialized=0,
        ProgramAuto=1,
        AperturePriority=2,
        ShutterPriority=3,
        Manual=4
    )
    _AEMeteringMode = Enum(
        Int8un,
        default=Pass,
        Uninitialized=0,
        Evaluative=1,
        CenterWeightedAverage=2,
        CenterArea=3,
        Spot=4
    )
    _FlashType = Enum(
        Int8un,
        default=Pass,
        Uninitialized=0,
        InternalPopupFlash=1,
        ExternalFlash=2
    )
    _FlashMode = Enum(
        Int8un,
        default=Pass,
        Normal=0,
        RedEyeReduction=0x01,
        FPEmission=0x02,
        MultiFlash=0x04,
        WirelessFlash1=0x08,
        WirelessFlash2=0x10,
        WirelessFlash3=0x20,
        SlowSynchronization=0x40,
    )
    _FlashSetting = Enum(
        Int8un,
        default=Pass,
        Uninitialized=0,
        TTLAuto=0x1,
        TTLManual=0x2,
        EmissionDisabled=0x80,
        ExposureWarning=0x81,
    )
    _WhiteBalance = Enum(
        Int8un,
        default=Pass,
        Uninitialized=0x0,
        Auto=0x1,
        Sunlight=0x2,
        Shade=0x3,
        Overcast=0x4,
        Incandescent=0x5,
        Fluorescent=0x6,
        Flash=0x7,
        Custom1=0x8,
        CustomCapture1=0x9,
        Custom2=0xA,
        CustomCapture2=0xB,
        Custom3=0xC,
        CustomCapture3=0xD,
        ColorTemparature=0x0E,
        LightSourcePriority=0x0F
    )
    _Resolution = Enum(
        Int8un,
        default=Pass,
        Uninitialized=0x0,
        High=0x1,
        Medium=0x2,
        Low=0x4
    )
    _ImageQuality = Enum(
        Int8un,
        default=Pass,
        JpegFine=0x2,
        JpegNormal=0x4,
        JpegBasic=0x8,
        Dng=0x10,
        DngAndJpeg=0x12
    )
    _CaptureMode = Enum(
        Int8un,
        default=Pass,
        Uninitialized=0x00,
        GeneralCapture=0x01,
        NonAFCapture=0x02,
        AFDriveOnly=0x03,
        StartAF=0x04,
        StopAF=0x05,
        StartCapture=0x06,
        StopCapture=0x07,
        StartRecodingMovieWithAF=0x10,
        StartRecodingMovieWithoutAF=0x20,
        StopRecodingMovie=0x30,
    )
    _CaptStatus = Enum(
        Int16ul,
        default=Pass,
        Cleared=0x0000, # Uninitialized / Cleared
        ShootingInProgress=0x0001, # Shooting standby / In operation
        ShootingSuccess=0x0002, # Shooting succeeded (Shooting sequence without image generation sequence)
        ImageGenerationInProgress=0x0004, # Image generation or custom white balance processing in progress
        ImageGenerationCompleted=0x0005, # Image data (file) generation completed
        StoppingMovieRecording=0x0006, # Preparation for stopping the movie recording
        MovieGenerationCompleted=0x0007, # Movie file generation completed
        AFSuccess=0x8001, # AF success (AFOnly mode only)
        CWBSuccess=0x8002, # Custom white balance acquirement succeeded (CWB Capture mode only).
        ImageDataStorageCompleted=0x8003, # Image data storage completed
        Interrupted=0x8004, # Other interrupt or exit without error (successfully exited)
        AFFailed=0x6001, # AF failure (in all shooting modes that use AF)
        BufferFull=0x6002,
        CWBFailed=0x6003, # Custom white balance image acquirement failed.
        ImageGenerationFailed=0x6004, # Image generation failed due to an error occurred during image generation.
        Failed=0x6005, # General failure (other than any of the above-mentioned failures.)
    )
    _DestinationToSave = Enum(
        Int8un,
        default=Pass,
        Uninitialized=0x00,
        InCamera=0x01, # In-camera media
        InComputer=0x02, # Drive in PC side
        Both=0x03, # In-camera media + Drive in PC side
    )

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

        self._CamCaptStatus = Struct(
            '_Header' / Int8un, # arbitrary value for parity
            'ImageId' / Int8un,
            'ImageDBHead' / Int8un,
            'ImageDBTail' / Int8un,
            'CaptStatus' / self._CaptStatus,
            'DestinationToSave' / self._DestinationToSave,
            '_Parity' / Int8un
        )

        self._SnapCommand = Struct(
            '_Header' / Default(Int8un, 0), # arbitrary value for parity
            'CaptureMode' / self._CaptureMode,
            'CaptureAmount' / Int8un,
            '_Parity' / Default(Int8un, 0)
        )

        super(SigmaPTP, self).__init__(*args, **kwargs)

    def _OperationCode(self, **vendor_operations):
        return super(SigmaPTP, self)._OperationCode(
            SigmaGetCamDataGroup1=0x9012,
            SigmaGetCamDataGroup2=0x9013,
            SigmaGetCamCaptStatus=0x9015,
            SigmaSetCamDataGroup1=0x9016,
            SigmaSetCamDataGroup2=0x9017,
            SigmaSnapCommand=0x901B,
            SigmaGetViewFrame=0x902B,
            SigmaConfigApi=0x9035,
            **vendor_operations
        )

    def _ResponseCode(self, **vendor_operations):
        return super(SigmaPTP, self)._ResponseCode(
            SigmaGetCamDataGroup1=0x9012,
            SigmaGetCamDataGroup2=0x9013,
            SigmaGetCamCaptStatus=0x9015,
            SigmaSetCamDataGroup1=0x9016,
            SigmaSetCamDataGroup2=0x9017,
            SigmaSnapCommand=0x901B,
            SigmaGetViewFrame=0x902B,
            SigmaConfigApi=0x9035,
            **vendor_operations
        )
