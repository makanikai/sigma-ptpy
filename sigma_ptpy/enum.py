"""Enumerations for SIGMA"""

from enum import IntEnum


class DirectoryType(IntEnum):
    UInt8 = 0x01
    String = 0x02
    UInt16 = 0x03
    UInt32 = 0x04
    URational = 0x05
    Int8 = 0x06
    Any8 = 0x07
    Int16 = 0x08
    Int32 = 0x09
    Rational = 0x0A
    Float32 = 0x0B
    Float64 = 0x0C


class ProgramShift(IntEnum):
    """The dial operation amount in the camera side is not reflected."""
    Null = 0  #: Uninitialized
    Plus = 0x01  #: PShift Plus (L_click)
    Minus = 0xff  #: PShift Minus (R_click)


class ISOAuto(IntEnum):
    Manual = 0
    Auto = 1


class ABSetting(IntEnum):
    Null = 0x00,
    AB3ZeroMinusPlus = 0x01  #: AB3: `0 → - → +`
    AB3MinusZeroPlus = 0x02  #: AB3: `- → 0 → +`
    AB3PlusZeroMinus = 0x03  #: AB3: `+ → 0 → -`
    AB5ZeroMinusPlus = 0x04  #: AB5: `0 → - → +`
    AB5MinusZeroPlus = 0x05  #: AB5: `- → 0 → +`
    AB5PlusZeroMinus = 0x06  #: AB5: `+ → 0 → -`


class DriveMode(IntEnum):
    Null = 0  #: Uninitialized
    SingleCapture = 1  #: Single Capture
    ContinuousCapture = 2  #: Continuous Capture
    TwoSecondsSelfTimer = 3  #: 2s Self Timer
    TenSecondsSelfTimer = 4  #: 10s Self Timer
    IntervalTimer = 7  #: Interval Timer


class SpecialMode(IntEnum):
    Null = 0x00  #: Uninitialized / None
    LiveView = 0x02  #: Live View Mode (Displays the live view in the PC side.)


class ExposureMode(IntEnum):
    Null = 0  #: Uninitialized
    ProgramAuto = 1  #: P
    AperturePriority = 2  #: A
    ShutterPriority = 3  #: S
    Manual = 4  #: M
    C1 = 0x10  #: C1
    C2 = 0x20  #: C2
    C3 = 0x40  #: C3
    Star = 0x80  #: I don't know what's this.


class AEMeteringMode(IntEnum):
    Null = 0  #: Uninitialized
    Evaluative = 1  #: Evaluative
    CenterWeightedAverage = 2  #: Center-weighted Average
    CenterArea = 3  #: Center Area
    Spot = 4  #: Spot


class FlashType(IntEnum):
    Null = 0
    InternalPopupFlash = 1  #: Internal pop-up flash
    ExternalFlash = 2  #: External Flash (SIGMA products Flash)


class FlashMode(IntEnum):
    Normal = 0  #: Uninitialized / Normal
    RedEyeReduction = 0x01
    FPEmission = 0x02
    MultiFlash = 0x04
    WirelessFlash1 = 0x08
    WirelessFlash2 = 0x10
    WirelessFlash3 = 0x20
    SlowSync = 0x40  #: Slow synchronization


class FlashSetting(IntEnum):
    Null = 0  #: Uninitialized
    TTLAuto = 0x1  #: TTL-Auto
    TTLManual = 0x2  #: TTL-Manual
    EmissionDisabled = 0x80  #: Emission disabled (charging in progress) * Read Only
    ExposureWarning = 0x81  #: Exposure warning (The strobe mark flashes.) * Read Only


class WhiteBalance(IntEnum):
    Null = 0x0
    Auto = 0x1
    Sunlight = 0x2
    Shade = 0x3
    Overcast = 0x4
    Incandescent = 0x5
    Fluorescent = 0x6
    Flash = 0x7
    Custom1 = 0x8
    CustomCapt1 = 0x9
    Custom2 = 0xA
    CustomCapt2 = 0xB
    Custom3 = 0xC
    CustomCapt3 = 0xD
    ColorTemp = 0x0E  #: Color Temperature
    LightSource = 0x0F  #: Auto (Light Source Priority)


class Resolution(IntEnum):
    Null = 0x0
    High = 0x1
    Medium = 0x2
    Low = 0x4


class ImageQuality(IntEnum):
    JPEGFine = 0x2
    JPEGNormal = 0x4
    JPEGBasic = 0x8
    DNG = 0x10
    DNGAndJPEG = 0x12


class ColorSpace(IntEnum):
    Null = 0x00
    sRGB = 0x01
    AdobeRGB = 0x02


class ColorMode(IntEnum):
    Normal = 0x00
    Sepia = 0x01
    Monochrome = 0x02
    Standard = 0x03
    Vivid = 0x04
    Neutral = 0x05
    Portrait = 0x06
    Landscape = 0x07
    FovClassicBlue = 0x08
    Sunset = 0x09
    Forest = 0x0A
    Cinema = 0x0B
    FovClassicYellow = 0x0C


class BatteryKind(IntEnum):
    Null = 0x00
    BodyBattery = 0x01
    ACAdapter = 0x02


class AFAuxLight(IntEnum):
    Null = 0x00
    On = 0x01
    Off = 0x02


class CaptureMode(IntEnum):
    Null = 0x00
    GeneralCapt = 0x01
    NonAFCapt = 0x02
    AFDriveOnly = 0x03
    StartAF = 0x04
    StopAF = 0x05
    StartCap = 0x06
    StopCapt = 0x07
    StartRecMovieAF = 0x10  #: Start Recording Movie with AF
    StartRecMovie = 0x20  #: Start Recording Movie without AF
    StopRecMovie = 0x30  #: Stop Recording Movie


class CaptStatus(IntEnum):
    Cleared = 0x0000  #: Uninitialized / Cleared
    ShootInProgress = 0x0001  #: Shooting standby / In operation
    ShootSuccess = 0x0002  #: Shooting succeeded (Shooting sequence without image generation sequence)
    ImageGenInProgress = 0x0004  #: Image generation or custom white balance processing in progress
    ImageGenCompleted = 0x0005  #: Image data (file) generation completed
    StopMovieRec = 0x0006  #: Preparation for stopping the movie recording
    MovieGenCompleted = 0x0007  #: Movie file generation completed
    AFSuccess = 0x8001  #: AF success (AFOnly mode only)
    CWBSuccess = 0x8002  #: Custom white balance acquirement succeeded (CWB Capture mode only).
    ImageDataStorageCompleted = 0x8003  #: Image data storage completed
    Interrupted = 0x8004  #: Other interrupt or exit without error (successfully exited)
    AFFailed = 0x6001  #: AF failure (in all shooting modes that use AF)
    BufferFull = 0x6002
    CWBFailed = 0x6003  #: Custom white balance image acquirement failed.
    ImageGenFailed = 0x6004  #: Image generation failed due to an error occurred during image generation.
    Failed = 0x6005  #: General failure (other than any of the above-mentioned failures.)


class DestToSave(IntEnum):
    Null = 0x00  #: Uninitialized
    InCamera = 0x01  #: In-camera media
    InComputer = 0x02  #: Drive in PC side
    Both = 0x03  #: In-camera media + Drive in PC side


class DCCropMode(IntEnum):
    Auto = 0x00  #: Uninitialized / AUTO
    Off = 0x01  #: OFF
    On = 0x02  #: ON


class LVMagnifyRatio(IntEnum):
    Null = 0x00  #: Uninitialized
    x1 = 0x01  #: x1.0
    x4 = 0x02  #: x4.0
    x8 = 0x03  #: x8.0


class HighISOExt(IntEnum):
    """High-sensitivity ISO extension"""
    Auto = 0x00  #: Uninitialized
    Off = 0x01  #: OFF
    On = 0x02  #: ON


class ContShootSpeed(IntEnum):
    """Continuous shooting speed"""
    Auto = 0x00  #: Uninitialized
    High = 0x01  #: High speed
    Medium = 0x02  #: Medium speed
    Low = 0x03  #: Low speed


class HDR(IntEnum):
    Null = 0x00  #: Uninitialized
    Off = 0xFF
    Auto = 0xFE
    PlusMinus1 = 0x01  #: ±1.0
    PlusMinus2 = 0x02  #: ±2.0
    PlusMinus3 = 0x03  #: ±3.0


class DNGQuality(IntEnum):
    Q12bit = 12  #: 12 bit quality
    Q14bit = 14  #: 14 bit quality


class LOCDistortion(IntEnum):
    """Lens Optics Compensation Distortion"""
    Null = 0x00  #: Uninitialized
    Auto = 0x01  #: AUTO
    Off = 0x02  #: OFF


class LOCChromaticAberration(IntEnum):
    """Lens Optics Compensation Chromatic Abberation"""
    Null = 0x00  #: Uninitialized
    Auto = 0x01  #: AUTO
    Off = 0x02  #: OFF


class LOCDiffraction(IntEnum):
    """Lens Optics Compensation Diffraction"""
    Null = 0x00  #: Uninitialized
    On = 0x01  #: ON
    Off = 0x02  #: OFF


class LOCVignetting(IntEnum):
    """Lens Optics Compensation Chromatic Abberation"""
    Null = 0x00  #: Uninitialized
    Auto = 0x01  #: AUTO
    Off = 0x02  #: OFF


class LOCColorShade(IntEnum):
    """Lens Optics Compensation Color Shading"""
    Null = 0x00  #: Uninitialized
    Auto = 0xFF  #: AUTO
    Off = 0xFE  #: OFF
    No1 = 0x01
    No2 = 0x02
    No3 = 0x03
    No4 = 0x04
    No5 = 0x05
    No6 = 0x06
    No7 = 0x07
    No8 = 0x08
    No9 = 0x09
    No10 = 0x0A


class LOCColorShadeAcq(IntEnum):
    """Lens Optics Compensation - Color Shading compensation value acquirement

    Leave it ON from the time you entered the compensation value capture menu using the camera or
    application operation until the time you exit the menu."""
    Null = 0x00  #: Uninitialized
    On = 0x01
    Off = 0x02


class EImageStab(IntEnum):
    """Electronic Image Stabilization"""
    Null = 0x00
    On = 0x01
    Off = 0x02


class AspectRatio(IntEnum):
    Null = 0x00  #: Uninitialized
    W21H9 = 0x01  #: 21:9
    W16H9 = 0x02  #: 16:9
    W3H2 = 0x03  #: 3:2
    W4H3 = 0x04  #: 4:3
    W7H6 = 0x05  #: 7:6
    W1H1 = 0x06  #: 1:1
    WSQRT2H1 = 0x07  #: sqrt(2):1


class ToneEffect(IntEnum):
    """Tone setting value in Monochrome mode"""
    Null = 0x00  #: Uninitialized
    BAndW = 0x01  #: B&W


class AFAuxLightEF(IntEnum):
    """Auxiliary light activation setting for external flash"""
    Null = 0x00  #: Uninitialized
    On = 0x01
    Off = 0x02


class FocusMode(IntEnum):
    MF = 1
    AF = 2
    AF_S = 3
    AF_C = 4


class AFLock(IntEnum):
    Off = 0
    On = 1


class FaceEyeAF(IntEnum):
    Off = 0
    FaceOnly = 1
    FaceEyeAuto = 2


class FaceEyeAFStatus(IntEnum):
    NonDetection = 0
    Detection = 1


class FocusArea(IntEnum):
    MultiAutoFocusPoints = 1
    OnePointSelection = 2
    Tracking = 3


class OnePointSelection(IntEnum):
    Free = 0
    X49 = 49


class PreConstAF(IntEnum):
    Off = 0
    On = 1


class FocusLimit(IntEnum):
    Off = 0
    On = 1
