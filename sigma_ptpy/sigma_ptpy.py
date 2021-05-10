import logging
from construct import Container
from ptpy import USB

from .enum import CaptureMode
from .schema import (
    _CamDataGroup1, _CamDataGroup2, _CamDataGroup3, _CamDataGroup4, _CamDataGroup5,
    _CamCaptStatus, _SnapCommand, _PictFileInfo2, _BigPartialPictFile,
    ApiConfig, CamDataGroupFocus
)
from .sigma_ptp import SigmaPTP


logger = logging.getLogger(__name__)


def _bytes_to_hex(b):
    return " ".join(list(map(lambda s: format(s, "02x"), b[:128])))


def _dict_to_payload_container(kwargs):
    field_present = dict((k, 1) for k in kwargs.keys())
    return Container(
        FieldPresent=Container(**field_present),
        **kwargs)


class SigmaPTPy(SigmaPTP, USB):
    """Operations on a SIGMA camera.

    Args:
        device (object): the USB device object.
        name (str): the name of USB devices for search.

    Examples:
        Usage as follows::

            from sigma_ptpy import SigmaPTPy

            camera = SigmaPTPy()

            with camera.session():
                 camera.config_api()
                 # Do something."""

    def __init__(self, *args, **kwargs):
        logger.debug("Init SigmaPTPy")
        super(SigmaPTPy, self).__init__(*args, **kwargs)

    def __recv(self, opcode, SchemaClass):
        ptp = Container(
            OperationCode=opcode,
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[0])
        response = self.recv(ptp)
        logger.debug("RECV {} {}".format(opcode, _bytes_to_hex(response.Data)))
        instance = SchemaClass()
        instance.decode(response.Data)
        return instance

    def __send(self, opcode, data):
        payload = data.encode()
        logger.debug("SEND {} {}".format(opcode, _bytes_to_hex(payload)))
        ptp = Container(
            OperationCode=opcode,
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[])
        return self.send(ptp, payload)

    def config_api(self):
        """This is the first instruction issued to the camera by the application that uses API.

        After this instruction has been received, another custom command can be received until
        the USB connection is shut down or the sgm_CloseApplication instruction is received.
        When this function is executed, API resets the camera setting to the default.
        (When API connection is closed, the camera setting returns to the setting value
        which the user specified before using API. However, the movie/still image setting
        is synchronized with the switch status.) Furthermore, API does not accept any
        operation other than the power-off operation.
        The data to be handled is based on the IFD structure.

        Returns:
            sigma_ptpy.schema.ApiConfig: the set of values obtained from a camera."""
        return self.__recv('SigmaConfigApi', ApiConfig)

    def get_cam_data_group1(self):
        """This instruction acquires DataGroup1 status information from the camera.

        The returned container has the following fields:

        - ``ShutterSpeed`` (:obj:`int`): Shutter speed (8-bit APEX step)
        - ``Aperture`` (:obj:`int`): Aperture (8-bit APEX step)
        - ``ProgramShift`` (:obj:`sigma_ptpy.enum.ProgramShift`): The dial operation amount in the camera side
          is not reflected.
        - ``ISOAuto`` (:obj:`sigma_ptpy.enum.ISOAuto`): ISO auto
        - ``ISOSpeed`` (:obj:`int`): ISO sensitivity (8-bit APEX step)
        - ``ExpComp`` (:obj:`int`): Exposure compensation (8-bit APEX step). When the exposure mode is P, S,
          or A, the exposure compensation value is output. If it is M, a difference from the correct exposure
          of AE is output. If the exposure bracket is provided, the exposure compensation value is output,
          including the exposure bracket compensation value. (cf. "ExpCompExcludeAB" in DataGroup1)
        - ``ABValue`` (:obj:`int`): Auto bracket value (8-bit APEX step)
        - ``ABSetting`` (:obj:`sigma_ptpy.enum.ABSetting`): Auto bracket setting
        - ``FrameBufferState`` (:obj:`int`): Free space of FrameBuffer (in camera) (Maximum number of shots)
        - ``MediaFreeSpace`` (:obj:`int`): Free space of recording media (Maximum number of shots) (16bit)
        - ``MediaStatus`` (:obj:`int`)
        - ``CurrentLensFocalLength`` (:obj:`float`)
        - ``BatteryState`` (:obj:`int`)
        - ``ABShotRemainNumber`` (:obj:`int`)
        - ``ExpCompExcludeAB`` (:obj:`int`)
        - ``FieldPresent``: Field existence
            - ``ShutterSpeed`` (:obj:`bool`): "ShutterSpeed" field exists, or not.
            - ``Aperture`` (:obj:`bool`): "Aperture" field exists, or not.
            - ``ProgramShift`` (:obj:`bool`): "ProgramShift" field exists, or not.
            - ``ISOAuto`` (:obj:`bool`): "ISOAuto" field exists, or not.
            - ``ISOSpeed`` (:obj:`bool`): "ISOSpeed" field exists, or not.
            - ``ExpComp`` (:obj:`bool`): "ExpComp" field exists, or not.
            - ``ABValue`` (:obj:`bool`): "ABValue" field exists, or not.
            - ``ABSetting`` (:obj:`bool`): "ABSetting" field exists, or not.
            - ``FrameBufferState`` (:obj:`bool`): "FrameBufferState" field exists, or not.
            - ``MediaFreeSpace`` (:obj:`bool`): "MediaFreeSpace" field exists, or not.
            - ``MediaStatus`` (:obj:`bool`): "MediaStatus" field exists, or not.
            - ``CurrentLensFocalLength`` (:obj:`bool`): "CurrentLensFocalLength" field exists, or not.
            - ``BatteryState`` (:obj:`bool`): "BatteryState" field exists, or not.
            - ``ABShotRemainNumber`` (:obj:`bool`): "ABShotRemainNumber" field exists, or not.
            - ``ExpCompExcludeAB`` (:obj:`bool`): "ExpCompExcludeAB" field exists, or not.

        Returns:
            construct.Container: CamDataGroup1 object."""
        return self.__get_cam_data_group('SigmaGetCamDataGroup1', _CamDataGroup1)

    def get_cam_data_group2(self):
        """This instruction acquires DataGroup2 status information from the camera.

        The returned container has the following fields:

        - ``DriveMode`` (:obj:`sigma_ptpy.enum.DriveMode`): Drive mode
        - ``SpecialMode`` (:obj:`sigma_ptpy.enum.SpecialMode`): Using LiveView or not
        - ``ExposureMode`` (:obj:`sigma_ptpy.enum.ExposureMode`): P, A, S, or M
        - ``AEMeteringMode`` (:obj:`sigma_ptpy.enum.AEMeteringMode`): Auto exposure setting
        - ``FlashType`` (:obj:`sigma_ptpy.enum.FlashType`): Flash type
        - ``FlashMode`` (:obj:`sigma_ptpy.enum.FlashMode`): Flash mode
        - ``FlashSeting`` (:obj:`sigma_ptpy.enum.FlashSetting`): Flash setting
        - ``WhiteBalance`` (:obj:`sigma_ptpy.enum.WhiteBalance`): White balance
        - ``Resolution`` (:obj:`sigma_ptpy.enum.Resolution`): Resolition
        - ``ImageQuality`` (:obj:`sigma_ptpy.enum.ImageQuality`): JPEG or DNG
        - ``FieldPresent``: Field existence
            - ``DriveMode`` (:obj:`bool`): "DriveMode" field exists, or not.
            - ``SpecialMode`` (:obj:`bool`): "SpecialMode" field exists, or not.
            - ``ExposureMode`` (:obj:`bool`): "ExposureMode" field exists, or not.
            - ``AEMeteringMode`` (:obj:`bool`): "AEMeteringMode" field exists, or not.
            - ``FlashType`` (:obj:`bool`): "FlashType" field exists, or not.
            - ``FlashMode`` (:obj:`bool`): "FlashMode" field exists, or not.
            - ``FlashSeting`` (:obj:`bool`): "FlashSeting" field exists, or not.
            - ``WhiteBalance`` (:obj:`bool`): "WhiteBalance" field exists, or not.
            - ``Resolution`` (:obj:`bool`): "Resolution" field exists, or not.
            - ``ImageQuality`` (:obj:`bool`): "ImageQuality" field exists, or not.

        Returns:
            construct.Container: CamDataGroup2 object."""
        return self.__get_cam_data_group('SigmaGetCamDataGroup2', _CamDataGroup2)

    def get_cam_data_group3(self):
        """This instruction acquires DataGroup3 status information from the camera.

        The returned container has the following fields:

        - ``ColorSpace`` (:obj:`sigma_ptpy.enum.ColorSpace`): sRGB or AdobeRGB
        - ``ColorMode`` (:obj:`sigma_ptpy.enum.ColorMode`): Color mode
        - ``BatteryKind`` (:obj:`sigma_ptpy.enum.BatteryKind`):
        - ``LensWideFocalLength`` (:obj:`float`): focal length in mm (Wide end)
        - ``LensTeleFocalLength`` (:obj:`float`): focal length in mm (Tele end)
        - ``AFAuxLight`` (:obj:`sigma_ptpy.enum.AFAuxLight`): AF auxiliary light ON or OFF
        - ``AFBeep`` (:obj:`int`): AF beep sound
        - ``TimerSound`` (:obj:`int`): Timer sound
        - ``DestToSave`` (:obj:`sigma_ptpy.enum.DestToSave`): Destination to save pictures
        - ``FieldPresent``: Field existence
            - ``ColorSpace`` (:obj:`bool`): "ColorSpace" field exists, or not.
            - ``ColorMode`` (:obj:`bool`): "ColorMode" field exists, or not.
            - ``BatteryKind`` (:obj:`bool`): "BatteryKind" field exists, or not.
            - ``LensWideFocalLength`` (:obj:`bool`): "LensWideFocalLength" field exists, or not.
            - ``LensTeleFocalLength`` (:obj:`bool`): "LensTeleFocalLength" field exists, or not.
            - ``AFAuxLight`` (:obj:`bool`): "AFAuxLight" field exists, or not.
            - ``AFBeep`` (:obj:`bool`): "AFBeep" field exists, or not.
            - ``TimerSound`` (:obj:`bool`): "TimerSound" field exists, or not.
            - ``DestToSave`` (:obj:`bool`): "DestToSave" field exists, or not.

        Returns:
            construct.Container: CamDataGroup3 object."""
        return self.__get_cam_data_group('SigmaGetCamDataGroup3', _CamDataGroup3)

    def get_cam_data_group4(self):
        """This instruction acquires DataGroup4 status information from the camera.

        The returned container has the following fields:

        - ``DCCropMode`` (:obj:`sigma_ptpy.enum.DCCropMode`): The DC Crop setting value and AUTO are judged
          depending on the attached lens.
        - ``LVMagnifyRatio`` (:obj:`sigma_ptpy.enum.LVMagnifyRatio``)
        - ``HighISOExt`` (:obj:`sigma_ptpy.enum.HighISOExt``): Setting value of high-sensitivity ISO extension
        - ``ContShootSpeed`` (:obj:`sigma_ptpy.enum.ContShootSpeed`): Setting value of continuous shooting speed
        - ``HDR`` (:obj:`sigma_ptpy.enum.HDR`):
        - ``DNGQuality`` (:obj:`sigma_ptpy.enum.DNGQuality`): DNG image quality
        - ``FillLight`` (:obj:`sigma_ptpy.enum.FillLight`): Setting value of Fill Light. Set the ±5.0 range
          in 0.1 increments, and enter 10 times the UI display value.
        - ``LOCDistortion`` (:obj:`sigma_ptpy.enum.LOCDistortion`):
          Lens Optics Compensation - Distortion setting value
        - ``LOCChromaticAberration`` (:obj:`sigma_ptpy.enum.LOCChromaticAberration`):
          Lens Optics Compensation - Chromatic Aberration setting value
        - ``LOCDiffraction`` (:obj:`sigma_ptpy.enum.LOCDiffraction`):
          Lens Optics Compensation - Diffraction setting value
        - ``LOCVignetting`` (:obj:`sigma_ptpy.enum.LOCVignetting`):
          Lens Optics Compensation - Vignetting setting value
        - ``LOCColorShade`` (:obj:`sigma_ptpy.enum.LOCColorShade`):
          Lens Optics Compensation - Color Shading setting value
        - ``LOCColorShadeAcq`` (:obj:`sigma_ptpy.enum.LOCColorShadeAcq`):
          Lens Optics Compensation - Color Shading compensation value acquirement.
          Leave it ON from the time you entered the compensation value capture menu using
          camera or application operation until the time you exit the menu.
        - ``EImageStab`` (:obj:`sigma_ptpy.enum.EImageStab`): Setting value of Electronic Image Stabilization
        - ``ShutterSound`` (:obj:`sigma_ptpy.enum.ShutterSound`): Shutter sound / Recording start/stop sound
        - ``FieldPresent``: Field existence
            - ``DCCropMode`` (:obj:`bool`): "DCCropMode" field exists, or not.
            - ``LVMagnifyRatio`` (:obj:`bool`): "LVMagnifyRatio" field exists, or not.
            - ``HighISOExt`` (:obj:`bool`): "HighISOExt" field exists, or not.
            - ``ContShootSpeed`` (:obj:`bool`): "ContShootSpeed" field exists, or not.
            - ``HDR`` (:obj:`bool`): "HDR" field exists, or not.
            - ``DNGQuality`` (:obj:`bool`): "DNGQuality" field exists, or not.
            - ``FillLight`` (:obj:`bool`): "FillLight" field exists, or not.
            - ``LOC`` (:obj:`bool`): "LOC*" fields exist, or not.
            - ``EImageStab`` (:obj:`bool`): "EImageStab" field exists, or not.
            - ``ShutterSound`` (:obj:`bool`): "ShutterSound" field exists, or not.

        Returns:
            construct.Container: CamDataGroup4 object."""
        return self.__get_cam_data_group('SigmaGetCamDataGroup4', _CamDataGroup4)

    def get_cam_data_group5(self):
        """This instruction acquires DataGroup5 status information from the camera.

        The returned container has the following fields:

        - ``IntervalTimerSecond`` (:obj:`int`): Shooting interval in Interval Timer mode (Unit in seconds)
        - ``IntervalTimerFrame`` (:obj:`int`): The number of shots in Interval Timer mode.
          0 indicates the infinite, and other numeric values indicate the specified number of shots.
        - ``IntervalTimerSecondRemain`` (:obj:`int`): Remaining time required to start the next
          shooting in Interval Timer mode (Unit in seconds)
        - ``IntervalTimerFrameRemain`` (:obj:`int`): Remaining time required to end shooting in Interval Timer mode
        - ``ColorTemp`` (:obj:`int`): User setting value of color temperature white balance (Unit in kelvin)
        - ``AspectRatio`` (:obj:`sigma_ptpy.enum.AspectRatio`): Aspect Ratio setting value
        - ``ToneEffect`` (:obj:`sigma_ptpy.enum.ToneEffect`): Tone setting value in Monochrome mode
        - ``AFAuxLightEF`` (:obj:`sigma_ptpy.enum.AFAuxLightEF`): Auxiliary light activation setting for external flash.
        - ``FieldPresent``: Field existence
            - ``IntervalTimer`` (:obj:`bool`): "IntervalTimer*" fields exist, or not.
            - ``ColorTemp`` (:obj:`bool`): "ColorTemp" field exists, or not.
            - ``AspectRatio`` (:obj:`bool`): "AspectRatio" field exists, or not.
            - ``ToneEffect`` (:obj:`bool`): "ToneEffect" field exists, or not.
            - ``AFAuxLightEF`` (:obj:`bool`): "AFAuxLightEF" field exists, or not.

        Returns:
            construct.Container: CamDataGroup5 object."""
        return self.__get_cam_data_group('SigmaGetCamDataGroup5', _CamDataGroup5)

    def __get_cam_data_group(self, opcode, schema):
        ptp = Container(
            OperationCode=opcode,
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[])
        response = self.recv(ptp)
        logger.debug("RECV {} {}".format(opcode, _bytes_to_hex(response.Data)))
        return self._parse_if_data(response, schema)

    def set_cam_data_group1(self, ShutterSpeed=None, Aperture=None, ProgramShift=None, ISOAuto=None, ISOSpeed=None,
                            ExpComp=None, ABValue=None, ABSetting=None):
        """This instruction changes DataGroup1 status information of the camera.

        Args:
            ShutterSpeed (int): Shutter speed (8-bit APEX step)
            Aperture (int): Aperture (8-bit APEX step)
            ProgramShift (sigma_ptpy.enum.ProgramShift): The dial operation amount in the camera side is not reflected.
            ISOAuto (sigma_ptpy.enum.ISOAuto): ISO auto
            ISOSpeed (int): ISO sensitivity (8-bit APEX step)
            ExpComp (int): Exposure compensation (8-bit APEX step)
                When the exposure mode is P, S, or A, the exposure compensation value is
                output. If it is M, a difference from the correct exposure of AE is output.
                If the exposure bracket is provided, the exposure compensation value is output,
                including the exposure bracket compensation value. (cf. "ExpCompExcludeAB" in DataGroup1)
            ABValue (int): Auto bracket value (8-bit APEX step)
            ABSetting (sigma_ptpy.enum.ABSetting): Auto bracket setting"""
        data = Container(
            _Header=0x0,
            FieldPresent=Container(
                ShutterSpeed=(ShutterSpeed is not None),
                Aperture=(Aperture is not None),
                ProgramShift=(ProgramShift is not None),
                ISOAuto=(ISOAuto is not None),
                ISOSpeed=(ISOSpeed is not None),
                ExpComp=(ExpComp is not None),
                ABValue=(ABValue is not None),
                ABSetting=(ABSetting is not None),
                CurrentLensFocalLength=False,
                FrameBufferState=False, MediaFreeSpace=False, MediaStatus=False,
                BatteryState=False, ABShotRemainNumber=False, ExpCompExcludeAB=False,
                _Reserved0=False,
            ),
            ShutterSpeed=ShutterSpeed,
            Aperture=Aperture,
            ProgramShift=ProgramShift,
            ISOAuto=ISOAuto,
            ISOSpeed=ISOSpeed,
            ExpComp=ExpComp,
            ABValue=ABValue,
            ABSetting=ABSetting,
            CurrentLensFocalLength=None,
            FrameBufferState=None, MediaFreeSpace=None, MediaStatus=None,
            BatteryState=None, ABShotRemainNumber=None, ExpCompExcludeAB=None,
            _Reserved0=None,
            _Parity=0,
        )
        return self.__set_cam_data_group('SigmaSetCamDataGroup1', _CamDataGroup1, data)

    def set_cam_data_group2(self, DriveMode=None, SpecialMode=None, ExposureMode=None, AEMeteringMode=None,
                            FlashMode=None, FlashSetting=None, WhiteBalance=None,
                            Resolution=None, ImageQuality=None):
        """This instruction changes DataGroup2 status information of the camera.

        Args:
            DriveMode (sigma_ptpy.enum.DriveMode): Drive mode
            SpecialMode (sigma_ptpy.enum.SpecialMode): Using LiveView or not
            ExposureMode (sigma_ptpy.enum.ExposureMode): P, A, S, or M
            AEMeteringMode (sigma_ptpy.enum.AEMeteringMode): Auto exposure setting
            FlashMode (sigma_ptpy.enum.FlashMode): Flash mode
            FlashSeting (sigma_ptpy.enum.FlashSetting): Flash setting
            WhiteBalance (sigma_ptpy.enum.WhiteBalance): White balance
            Resolution (sigma_ptpy.enum.Resolution): Resolition
            ImageQuality (sigma_ptpy.enum.ImageQuality): JPEG or DNG"""
        data = Container(
            _Header=0,
            FieldPresent=Container(
                DriveMode=(DriveMode is not None),
                SpecialMode=(SpecialMode is not None),
                ExposureMode=(ExposureMode is not None),
                AEMeteringMode=(AEMeteringMode is not None),
                FlashMode=(FlashMode is not None),
                FlashSetting=(FlashSetting is not None),
                WhiteBalance=(WhiteBalance is not None),
                Resolution=(Resolution is not None),
                ImageQuality=(ImageQuality is not None),
                _Reserved0=False, _Reserved1=False, _Reserved2=False,
                _Reserved3=False, _Reserved4=False, _Reserved5=False,
                FlashType=False,
            ),
            DriveMode=DriveMode,
            SpecialMode=SpecialMode,
            ExposureMode=ExposureMode,
            AEMeteringMode=AEMeteringMode,
            FlashMode=FlashMode,
            FlashSetting=FlashSetting,
            WhiteBalance=WhiteBalance,
            Resolution=Resolution,
            ImageQuality=ImageQuality,
            _Reserved0=None, _Reserved1=None, _Reserved2=None,
            _Reserved3=None, _Reserved4=None, _Reserved5=None,
            FlashType=False,
            _Parity=0,
        )
        print(data)
        return self.__set_cam_data_group('SigmaSetCamDataGroup2', _CamDataGroup2, data)

    def set_cam_data_group3(self, ColorSpace=None, ColorMode=None, AFAuxLight=None,
                            AFBeep=None, TimerSound=None, DestToSave=None):
        """This instruction changes DataGroup3 status information of the camera.

        Args:
            ColorSpace (sigma_ptpy.enum.ColorSpace): sRGB or AdobeRGB
            ColorMode (sigma_ptpy.enum.ColorMode): Color mode
            AFAuxLight (sigma_ptpy.enum.AFAuxLight): AF auxiliary light ON or OFF
            AFBeep (int): AF beep sound
            TimerSound (int): Timer sound
            DestToSave (sigma_ptpy.enum.DestToSave): Destination to save pictures"""
        data = Container(
            _Header=0x0,
            FieldPresent=Container(
                ColorSpace=(ColorSpace is not None),
                ColorMode=(ColorMode is not None),
                AFAuxLight=(AFAuxLight is not None),
                AFBeep=(AFBeep is not None),
                TimerSound=(TimerSound is not None),
                DestToSave=(DestToSave is not None),
                BatteryKind=False, LensWideFocalLength=False, LensTeleFocalLength=False,
                _Reserved0=False, _Reserved1=False, _Reserved2=False, _Reserved3=False,
                _Reserved4=False, _Reserved5=False, _Reserved6=False,
            ),
            ColorSpace=ColorSpace,
            ColorMode=ColorMode,
            AFAuxLight=AFAuxLight,
            AFBeep=AFBeep,
            TimerSound=TimerSound,
            DestToSave=DestToSave,
            BatteryKind=None, LensWideFocalLength=None, LensTeleFocalLength=None,
            _Reserved0=None, _Reserved1=None, _Reserved2=None, _Reserved3=None,
            _Reserved4=None, _Reserved5=None, _Reserved6=None,
            _Parity=0,
        )
        return self.__set_cam_data_group('SigmaSetCamDataGroup3', _CamDataGroup3, data)

    def set_cam_data_group4(self, DCCropMode=None, LVMagnifyRatio=None, HighISOExt=None,
                            ContShootSpeed=None, HDR=None, DNGQuality=None, FillLight=None,
                            LOCDistortion=None, LOCChromaticAbberation=None, LOCDiffraction=None,
                            LOCVignetting=None, LOCColorShade=None, LOCColorShadeAcq=None,
                            EImageStab=None, ShutterSound=None):
        """This instruction changes DataGroup4 status information of the camera.

        Args:
            DCCropMode (sigma_ptpy.enum.DCCropMode): The DC Crop setting value and AUTO are judged
                depending on the attached lens.
            LVMagnifyRatio (sigma_ptpy.enum.LVMagnifyRatio):
            HighISOExt (sigma_ptpy.enum.HighISOExt): Setting value of high-sensitivity ISO extension
            ContShootSpeed (sigma_ptpy.enum.ContShootSpeed): Setting value of continuous shooting speed
            HDR (sigma_ptpy.enum.HDR):
            DNGQuality (sigma_ptpy.enum.DNGQuality): DNG image quality
            FillLight (sigma_ptpy.enum.FillLight): Setting value of Fill Light
                Set the ±5.0 range in 0.1 increments, and enter 10 times the UI display value.
            LOCDistortion (sigma_ptpy.enum.LOCDistortion): Lens Optics Compensation - Distortion setting value
            LOCChromaticAberration (sigma_ptpy.enum.LOCChromaticAberration): Lens Optics Compensation -
                Chromatic Aberration setting value
            LOCDiffraction (sigma_ptpy.enum.LOCDiffraction): Lens Optics Compensation - Diffraction setting value
            LOCVignetting (sigma_ptpy.enum.LOCVignetting): Lens Optics Compensation - Vignetting setting value
            LOCColorShade (sigma_ptpy.enum.LOCColorShade): Lens Optics Compensation - Color Shading setting value
            LOCColorShadeAcq (sigma_ptpy.enum.LOCColorShadeAcq): Lens Optics Compensation -
                Color Shading compensation value acquirement.
                Leave it ON from the time you entered the compensation value capture menu using
                camera or application operation until the time you exit the menu.
            EImageStab (sigma_ptpy.enum.EImageStab): Setting value of Electronic Image Stabilization
            ShutterSound (sigma_ptpy.enum.ShutterSound): Shutter sound / Recording start/stop sound"""
        LOC = LOCDistortion is not None or LOCChromaticAbberation is not None or LOCDiffraction is not None \
            or LOCVignetting is not None or LOCColorShade is not None or LOCColorShadeAcq is not None
        data = Container(
            _Header=0x0,
            FieldPresent=Container(
                DCCropMode=(DCCropMode is not None),
                LVMagnifyRatio=(LVMagnifyRatio is not None),
                HighISOExt=(HighISOExt is not None),
                ContShootSpeed=(ContShootSpeed is not None),
                HDR=(HDR is not None),
                DNGQuality=(DNGQuality is not None),
                FillLight=(FillLight is not None),
                EImageStab=(EImageStab is not None),
                ShutterSound=(ShutterSound is not None),
                LOC=LOC,
                _Reserved0=False, _Reserved1=False, _Reserved2=False,
                _Reserved3=False, _Reserved4=False, _Reserved5=False,
            ),
            DCCropMode=DCCropMode,
            LVMagnifyRatio=LVMagnifyRatio,
            HighISOExt=HighISOExt,
            ContShootSpeed=ContShootSpeed,
            HDR=HDR,
            DNGQuality=DNGQuality,
            FillLight=FillLight,
            EImageStab=EImageStab,
            ShutterSound=ShutterSound,
            LOCDistortion=(LOCDistortion or 0 if LOC else None),
            LOCChromaticAbberation=(LOCChromaticAbberation or 0 if LOC else None),
            LOCDiffraction=(LOCDiffraction or 0 if LOC else None),
            LOCVignetting=(LOCVignetting or 0 if LOC else None),
            LOCColorShade=(LOCColorShade or 0 if LOC else None),
            LOCColorShadeAcq=(LOCColorShadeAcq or 0 if LOC else None),
            _Reserved0=None, _Reserved1=None, _Reserved2=None,
            _Reserved3=None, _Reserved4=None, _Reserved5=None,
            _Parity=0,
        )
        return self.__set_cam_data_group('SigmaSetCamDataGroup4', _CamDataGroup4, data)

    def set_cam_data_group5(self, IntervalTimerSecond=None, IntervalTimerFrame=None,
                            ColorTemp=None, AspectRatio=None, ToneEffect=None, AFAuxLightEF=None):
        """This instruction changes DataGroup5 status information of the camera.

        When you set Interval Timer mode, both of IntervalTimerSecond and IntervalTimerFrame must
        be given at the same time.

        Args:
            IntervalTimerSecond (int): Shooting interval in Interval Timer mode (Unit in seconds)
            IntervalTimerFrame (int): The number of shots in Interval Timer mode.
                0 indicates the infinite, and other numeric values indicate the specified number of shots.
            ColorTemp (int): User setting value of color temperature white balance (Unit in kelvin)
            AspectRatio (sigma_ptpy.enum.AspectRatio): Aspect Ratio setting value
            ToneEffect (sigma_ptpy.enum.ToneEffect): Tone setting value in Monochrome mode
            AFAuxLightEF (sigma_ptpy.enum.AFAuxLightEF): Auxiliary light activation setting for external flash"""
        if (IntervalTimerSecond is not None) != (IntervalTimerFrame is not None):
            raise ValueError("both of IntervalTimerSecond and IntervalTimerFrame must be given.")

        data = Container(
            _Header=0x0,
            FieldPresent=Container(
                IntervalTimer=(IntervalTimerSecond is not None),
                ColorTemp=(ColorTemp is not None),
                AspectRatio=(AspectRatio is not None),
                ToneEffect=(ToneEffect is not None),
                AFAuxLightEF=(AFAuxLightEF is not None),
                _Reserved0=False, _Reserved1=False, _Reserved2=False, _Reserved3=False,
                _Reserved4=False, _Reserved5=False, _Reserved6=False, _Reserved7=False,
                _Reserved8=False, _Reserved9=False, _Reserved10=False,
            ),
            IntervalTimerSecond=IntervalTimerSecond,
            IntervalTimerFrame=IntervalTimerFrame,
            IntervalTimerSecondRemain=0,
            IntervalTimerFrameRemain=0,
            ColorTemp=ColorTemp,
            AspectRatio=AspectRatio,
            ToneEffect=ToneEffect,
            AFAuxLightEF=AFAuxLightEF,
            _Reserved0=None, _Reserved1=None, _Reserved2=None, _Reserved3=None,
            _Reserved4=None, _Reserved5=None, _Reserved6=None, _Reserved7=None,
            _Reserved8=None, _Reserved9=None, _Reserved10=None, _Parity=0
        )
        return self.__set_cam_data_group('SigmaSetCamDataGroup5', _CamDataGroup5, data)

    def __set_cam_data_group(self, opcode, schema, data):
        payload = self._build_if_not_data(data, schema)
        logger.debug("SEND {} {}".format(opcode, _bytes_to_hex(payload)))
        ptp = Container(
            OperationCode=opcode,
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[])
        return self.send(ptp, payload)

    def get_cam_data_group_focus(self):
        """This function notifies the PC of the camera setting value.
        The data to be handled is based on the IFD structure.

        Returns:
            sigma_ptpy.schema.CamDataGroupFocus: the set of values obtained from a camera."""
        return self.__recv('SigmaGetCamDataGroupFocus', CamDataGroupFocus)

    def set_cam_data_group_focus(self, focus):
        """This function changes the camera setting value from the PC.
        The data to be handled is based on the IFD structure.

        Args:
            focus (sigma_ptpy.schema.CamDataGroupFocus): the set of values to be sent."""
        return self.__send('SigmaSetCamDataGroupFocus', focus)

    def get_cam_capt_status(self):
        """This instruction acquires the shooting result from the camera.

        Returns:
            construct.Container: CamCaptStatus object."""
        ptp = Container(
            OperationCode='SigmaGetCamCaptStatus',
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[0x00000000])
        response = self.recv(ptp)
        logger.debug("RECV SigmaGetCamCaptStatus {}".format(_bytes_to_hex(response.Data)))
        return self._parse_if_data(response, _CamCaptStatus)

    def get_pict_file_info2(self):
        """This function requests information of the data (image file) that is shot in Camera Control mode.

        Returns:
            construct.Container: PictFileInfo2 object."""
        ptp = Container(
            OperationCode='SigmaGetPictFileInfo2',
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[])
        response = self.recv(ptp)
        logger.debug("RECV SigmaGetPictFileInfo2 {}".format(_bytes_to_hex(response.Data)))
        return self._parse_if_data(response, _PictFileInfo2)

    def get_view_frame(self):
        """"This function acquires image data when displaying LiveView.

        When LiveView or QuickView can be prepared, the camera transfers image data to the PC;
        otherwise, it transfers data, which means that the target image is not found, to the PC.
        This function does not ensure checksum data to display LiveView images as much as possible.

        Returns:
            bytes: a JPEG image.

        Examples:
            You can obtain a RGB array from a returned JPEG data as follows::

                pict = camera.get_view_frame()
                img = cv2.imdecode(np.frombuffer(pict, np.uint8), cv2.IMREAD_COLOR)"""

        ptp = Container(
            OperationCode='SigmaGetViewFrame',
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[])
        response = self.recv(ptp)
        return response.Data[10:]

    def snap_command(self, CaptureMode=CaptureMode.GeneralCapt, CaptureAmount=1):
        """This command issues shooting instructions from the PC to the camera.

        Args:
            CaptureMode (sigma_ptpy.enum.CaptureMode): Capture mode
            CaptureAmount (int): the number of continuous shots."""
        data = Container(
            _Header=0x03,
            CaptureMode=CaptureMode,
            CaptureAmount=CaptureAmount,
            _Parity=0,
        )
        payload = self._build_if_not_data(data, _SnapCommand)
        ptp = Container(
            OperationCode='SigmaSnapCommand',
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[])
        return self.send(ptp, payload)

    def get_big_partial_pict_file(self, store_address, start_address, max_length):
        """This function downloads image data (image file) shot by the camera in pieces.

        Args:
            store_address (int): Image file storage location address (head address)
            start_address (int): Image file transfer starting position (offset address)
            max_length (int): Image file transfer size (units: bytes / Maximum value: 0x8000000)

        Returns:
            construct.Container: BigPartialPictFile object."""
        ptp = Container(
            OperationCode='SigmaGetBigPartialPictFile',
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[store_address, start_address, max_length])
        response = self.recv(ptp)
        return self._parse_if_data(response, _BigPartialPictFile)
