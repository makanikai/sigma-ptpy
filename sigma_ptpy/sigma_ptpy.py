import logging
import usb.core
from construct import Container
from ptpy import USB
from .schema import (
    ApiConfig, CamDataGroup1, CamDataGroup2, CamDataGroup3, CamDataGroup4, CamDataGroup5,
    CamDataGroupFocus, CamCanSetInfo5, CamCaptStatus,
    SnapCommand, PictFileInfo2, BigPartialPictFile, ViewFrame)
from .sigma_ptp import SigmaPTP


logger = logging.getLogger(__name__)


def _bytes_to_hex(b):
    return " ".join(list(map(lambda s: format(s, "02x"), b[:128])))


class SigmaPTPy(SigmaPTP, USB):
    """Operations on a SIGMA camera.

    Args:
        device (object): the USB device object.
        name (str): the name of USB devices for search.
        ignore_events (bool):

    Examples:
        Usage as follows::

            from sigma_ptpy import SigmaPTPy

            camera = SigmaPTPy()

            with camera.session():
                 camera.config_api()
                 # Do something.
                 camera.close_application()"""

    def __init__(self, *args, ignore_events=False, **kwargs):
        logger.debug("Init SigmaPTPy")
        super(SigmaPTPy, self).__init__(*args, **kwargs)

        if ignore_events:
            # bad operation for ignoring PTP events
            self._USBTransport__event_shutdown.set()
            if self._USBTransport__event_proc.is_alive():
                self._USBTransport__event_proc.join(2)

    def __recv(self, opcode, klass, params=[], timeout=None):
        _timeout = None
        # bad operation for setting timeout
        if timeout is not None:
            _timeout = self._USBTransport__inep.device._Device__default_timeout
            self._USBTransport__inep.device._Device__default_timeout = timeout

        ptp = Container(
            OperationCode=opcode,
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=params)
        response = self.recv(ptp)
        logger.debug("RECV {} {}".format(opcode, _bytes_to_hex(response.Data)))

        if _timeout is not None:
            self._USBTransport__inep.device._Device__default_timeout = _timeout

        instance = klass()
        instance.decode(response.Data)
        return instance

    def __send(self, opcode, klass, data):
        if not isinstance(data, klass):
            raise TypeError("{} is expected, but {} is given".format(klass, type(data)))

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
        return self.__recv('SigmaConfigApi', ApiConfig, params=[0])

    def close_application(self):
        """This instruction informs the camera that the session is closed when the application exits."""
        logger.debug("SEND SigmaCloseApplication")
        payload = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"  # This payload is undocumented. What's this?
        ptp = Container(
            OperationCode='SigmaCloseApplication',
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[])
        return self.send(ptp, payload)

    def get_cam_data_group1(self):
        """This instruction acquires DataGroup1 status information from the camera.

        Returns:
            sigma_ptpy.schema.CamDataGroup1: CamDataGroup1 object."""
        return self.__recv('SigmaGetCamDataGroup1', CamDataGroup1)

    def get_cam_data_group2(self):
        """This instruction acquires DataGroup2 status information from the camera.

        Returns:
            sigma_ptpy.schema.CamDataGroup2: CamDataGroup2 object."""
        return self.__recv('SigmaGetCamDataGroup2', CamDataGroup2)

    def get_cam_data_group3(self):
        """This instruction acquires DataGroup3 status information from the camera.

        Returns:
            sigma_ptpy.schema.CamDataGroup3: CamDataGroup3 object."""
        return self.__recv('SigmaGetCamDataGroup3', CamDataGroup3)

    def get_cam_data_group4(self):
        """This instruction acquires DataGroup4 status information from the camera.

        Returns:
            sigma_ptpy.schema.CamDataGroup4: CamDataGroup4 object."""
        return self.__recv('SigmaGetCamDataGroup4', CamDataGroup4)

    def get_cam_data_group5(self):
        """This instruction acquires DataGroup5 status information from the camera.

        Returns:
            sigma_ptpy.schema.CamDataGroup5: CamDataGroup5 object."""
        return self.__recv('SigmaGetCamDataGroup5', CamDataGroup5)

    def set_cam_data_group1(self, data):
        """This instruction changes DataGroup1 status information of the camera.

        Args:
            data (sigma_ptpy.schema.CamDataGroup1): DataGroup1 status information"""
        return self.__send('SigmaSetCamDataGroup1', CamDataGroup1, data)

    def set_cam_data_group2(self, data):
        """This instruction changes DataGroup2 status information of the camera.

        Args:
            data (sigma_ptpy.schema.CamDataGroup2): DataGroup2 status information"""
        return self.__send('SigmaSetCamDataGroup2', CamDataGroup2, data)

    def set_cam_data_group3(self, data):
        """This instruction changes DataGroup3 status information of the camera.

        Args:
            data (sigma_ptpy.schema.CamDataGroup3): DataGroup3 status information"""
        return self.__send('SigmaSetCamDataGroup3', CamDataGroup3, data)

    def set_cam_data_group4(self, data):
        """This instruction changes DataGroup4 status information of the camera.

        Args:
            data (sigma_ptpy.schema.CamDataGroup4): DataGroup4 status information"""
        return self.__send('SigmaSetCamDataGroup4', CamDataGroup4, data)

    def set_cam_data_group5(self, data):
        """This instruction changes DataGroup5 status information of the camera.

        When you set Interval Timer mode, both of IntervalTimerSecond and IntervalTimerFrame must
        be given at the same time.

        Args:
            data (sigma_ptpy.schema.CamDataGroup5): DataGroup5 status information"""
        return self.__send('SigmaSetCamDataGroup5', CamDataGroup5, data)

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
        return self.__send('SigmaSetCamDataGroupFocus', CamDataGroupFocus, focus)

    def get_cam_can_set_info5(self):
        """This instruction acquires the setting items, which can be changed through the PC, from the camera.

        Returns:
            sigma_ptpy.schema.CamCanSetInfo5: the set of values obtained from a camera."""
        return self.__recv('SigmaGetCamCanSetInfo5', CamCanSetInfo5)

    def get_cam_capt_status(self, image_id):
        """This instruction acquires the shooting result from the camera.

        Args:
            image_id (int): the image ID to obtain a status.

        Returns:
            sigma_ptpy.schema.CamCaptStatus: CamCaptStatus object."""
        return self.__recv('SigmaGetCamCaptStatus', CamCaptStatus, params=[image_id])

    def get_pict_file_info2(self):
        """This function requests information of the data (image file) that is shot in Camera Control mode.

        Returns:
            sigma_ptpy.schema.PictFileInfo2: PictFileInfo2 object."""
        return self.__recv('SigmaGetPictFileInfo2', PictFileInfo2)

    def get_view_frame(self):
        """"This function acquires image data when displaying LiveView.

        When LiveView or QuickView can be prepared, the camera transfers image data to the PC;
        otherwise, it transfers data, which means that the target image is not found, to the PC.
        This function does not ensure checksum data to display LiveView images as much as possible.

        Returns:
            sigma_ptpy.schema.ViewFrame: a JPEG image.

        Examples:
            You can obtain a RGB array from a returned JPEG data as follows::

                pict = camera.get_view_frame()
                img = cv2.imdecode(np.frombuffer(pict.Data, np.uint8), cv2.IMREAD_COLOR)"""
        return self.__recv('SigmaGetViewFrame', ViewFrame)

    def snap_command(self, data):
        """This command issues shooting instructions from the PC to the camera.

        Args:
            data (sigma_ptpy.schema.SnapCommand): a snap command object."""
        return self.__send('SigmaSnapCommand', SnapCommand, data)

    def clear_image_db_single(self, image_id):
        """This instruction requests to clear the shooting result of the CaptStatus database in the camera."""
        logger.debug("SEND SigmaClearImageDBSingle")
        payload = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"  # This payload is undocumented. What's this?
        ptp = Container(
            OperationCode='SigmaClearImageDBSingle',
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[image_id])
        return self.send(ptp, payload)

    def get_big_partial_pict_file(self, store_address, start_address, max_length, timeout=5000):
        """This function downloads image data (image file) shot by the camera in pieces.

        Args:
            store_address (int): Image file storage location address (head address)
            start_address (int): Image file transfer starting position (offset address)
            max_length (int): Image file transfer size (units: bytes / Maximum value: 0x8000000)

        Returns:
            sigma_ptpy.schema.BigPartialPictFile: BigPartialPictFile object."""
        return self.__recv('SigmaGetBigPartialPictFile', BigPartialPictFile,
                           params=[store_address, start_address, max_length],
                           timeout=timeout)
