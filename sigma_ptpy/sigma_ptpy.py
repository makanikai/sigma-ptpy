import logging
from construct import Container
from ptpy import USB

from .enum import CaptureMode
from .schema import (
    _CamDataGroup1, _CamDataGroup2, _CamDataGroup3,
    _CamCaptStatus, _SnapCommand, _PictFileInfo2, _BigPartialPictFile
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
        logger.info("Init SigmaPTPy")
        super(SigmaPTPy, self).__init__(*args, **kwargs)

    def config_api(self):
        """This is the first instruction issued to the camera by the application that uses API.

        After this instruction has been received, another custom command can be received until
        the USB connection is shut down or the sgm_CloseApplication instruction is received.
        When this function is executed, API resets the camera setting to the default.
        (When API connection is closed, the camera setting returns to the setting value
        which the user specified before using API. However, the movie/still image setting
        is synchronized with the switch status.) Furthermore, API does not accept any
        operation other than the power-off operation.
        The data to be handled is based on the IFD structure."""
        data = Container(
            OperationCode='SigmaConfigApi',
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[0])
        return self.recv(data)

    def get_cam_data_group1(self):
        """This instruction acquires DataGroup1 status information from the camera.

        Returns:
            construct.Container: CamDataGroup1 object."""
        return self.__get_cam_data_group('SigmaGetCamDataGroup1', _CamDataGroup1)

    def get_cam_data_group2(self):
        """This instruction acquires DataGroup2 status information from the camera.

        Returns:
            construct.Container: CamDataGroup2 object."""
        return self.__get_cam_data_group('SigmaGetCamDataGroup2', _CamDataGroup2)

    def get_cam_data_group3(self):
        """This instruction acquires DataGroup3 status information from the camera.

        Returns:
            construct.Container: CamDataGroup3 object."""
        return self.__get_cam_data_group('SigmaGetCamDataGroup3', _CamDataGroup3)

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
                            ExpCompensation=None, ABValue=None, ABSetting=None, CurrentLensFocalLength=None):
        """This instruction changes DataGroup1 status information of the camera.

        Args:
            ShutterSpeed (int): Shutter speed (8-bit APEX step)
            Aperture (int): Aperture (8-bit APEX step)
            ProgramShift (sigma_ptpy.enum.ProgramShift): The dial operation amount in the camera side is not reflected.
            ISOAuto (sigma_ptpy.enum.ISOAuto): ISO auto
            ISOSpeed (int): ISO sensitivity (8-bit APEX step)
            ExpCompensation (int): Exposure compensation (8-bit APEX step)
                When the exposure mode is P, S, or A, the exposure compensation value is
                output. If it is M, a difference from the correct exposure of AE is output.
                If the exposure bracket is provided, the exposure compensation value is output,
                including the exposure bracket compensation value. (cf. "ExpCompExcludeAB" in DataGroup1)
            ABValue (int): Auto bracket value (8-bit APEX step)
            ABSetting (sigma_ptpy.enum.ABSetting): Auto bracket setting
            CurrentLensFocalLength (float): Focal length in mm"""
        data = Container(
            _Header=0x03,
            FieldPresent=Container(
                ShutterSpeed=(ShutterSpeed is not None),
                Aperture=(Aperture is not None),
                ProgramShift=(ProgramShift is not None),
                ISOAuto=(ISOAuto is not None),
                ISOSpeed=(ISOSpeed is not None),
                ExpCompensation=(ExpCompensation is not None),
                ABValue=(ABValue is not None),
                ABSetting=(ABSetting is not None),
                CurrentLensFocalLength=(CurrentLensFocalLength is not None),
                FrameBufferState=False, MediaFreeSpace=False, MediaStatus=False,
                BatteryState=False, ABShotRemainNumber=False, ExpCompExcludeAB=False,
                _Reserved0=False,
            ),
            ShutterSpeed=ShutterSpeed,
            Aperture=Aperture,
            ProgramShift=ProgramShift,
            ISOAuto=ISOAuto,
            ISOSpeed=ISOSpeed,
            ExpCompensation=ExpCompensation,
            ABValue=ABValue,
            ABSetting=ABSetting,
            CurrentLensFocalLength=CurrentLensFocalLength,
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
            _Header=0x03,
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
            _Header=0x03,
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

    def __set_cam_data_group(self, opcode, schema, data):
        payload = self._build_if_not_data(data, schema)
        logger.debug("SEND {} {}".format(opcode, _bytes_to_hex(payload)))
        ptp = Container(
            OperationCode=opcode,
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[])
        return self.send(ptp, payload)

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
