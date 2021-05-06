import logging
import sys
import os
from construct import Container
from ptpy import USB
from rainbow_logging_handler import RainbowLoggingHandler
from .enum import CaptureMode
from .schema import (
    _CamDataGroup1, _CamDataGroup2, _CamDataGroup3,
    _CamCaptStatus, _SnapCommand, _PictFileInfo2, _BigPartialPictFile
)
from .ptp import SigmaPTP

logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    '%(levelname).1s '
    '%(relativeCreated)d '
    '%(name)s'
    '[%(threadName)s:%(funcName)s:%(lineno)s] '
    '%(message)s'
)
level = "DEBUG" if "SIGMAPTPY_DEBUG" in os.environ else "INFO"

handler = RainbowLoggingHandler(sys.stderr)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(level)


def bytes_to_hex(b):
    return " ".join(list(map(lambda s: format(s, "02x"), b[:128])))


def dict_to_payload_container(kwargs):
    field_present = dict((k, 1) for k in kwargs.keys())
    return Container(
        FieldPresent=Container(**field_present),
        **kwargs)


class SigmaPTPy(SigmaPTP, USB):
    """Operations on the SIGMA fp series.

    Args:
        device (object): the USB device object.
        name (str): the name of USB devices for search."""

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
        return self._get_cam_data_group('SigmaGetCamDataGroup1', _CamDataGroup1)

    def get_cam_data_group2(self):
        return self._get_cam_data_group('SigmaGetCamDataGroup2', _CamDataGroup2)

    def get_cam_data_group3(self):
        return self._get_cam_data_group('SigmaGetCamDataGroup3', _CamDataGroup3)

    def _get_cam_data_group(self, opcode, schema):
        ptp = Container(
            OperationCode=opcode,
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[])
        response = self.recv(ptp)
        logger.debug("RECV {} {}".format(opcode, bytes_to_hex(response.Data)))
        return self._parse_if_data(response, schema)

    def set_cam_data_group1(self, **kwargs):
        return self._set_cam_data_group('SigmaSetCamDataGroup1', _CamDataGroup1, kwargs)

    def set_cam_data_group2(self, **kwargs):
        return self._set_cam_data_group('SigmaSetCamDataGroup2', _CamDataGroup2, kwargs)

    def set_cam_data_group3(self, **kwargs):
        return self._set_cam_data_group('SigmaSetCamDataGroup3', _CamDataGroup3, kwargs)

    def _set_cam_data_group(self, opcode, schema, kwargs):
        data = dict_to_payload_container(kwargs)
        payload = self._build_if_not_data(data, schema)
        logger.debug("SEND {} {}".format(opcode, bytes_to_hex(payload)))
        ptp = Container(
            OperationCode=opcode,
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[])
        return self.send(ptp, payload)

    def get_cam_capt_status(self):
        ptp = Container(
            OperationCode='SigmaGetCamCaptStatus',
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[0x00000000])
        response = self.recv(ptp)
        logger.debug("RECV SigmaGetCamCaptStatus {}".format(bytes_to_hex(response.Data)))
        return self._parse_if_data(response, _CamCaptStatus)

    def get_pict_file_info2(self):
        ptp = Container(
            OperationCode='SigmaGetPictFileInfo2',
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[])
        response = self.recv(ptp)
        logger.debug("RECV SigmaGetPictFileInfo2 {}".format(bytes_to_hex(response.Data)))
        return self._parse_if_data(response, _PictFileInfo2)

    def get_view_frame(self):
        '''Load a live-view image from a camera.'''

        ptp = Container(
            OperationCode='SigmaGetViewFrame',
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[])
        response = self.recv(ptp)
        return response.Data[10:]

    def snap_command(self, capture_mode=CaptureMode.GeneralCapt, capture_amount=1):
        data = Container(
            CaptureMode=capture_mode,
            CaptureAmount=capture_amount
        )
        payload = self._build_if_not_data(data, _SnapCommand)
        ptp = Container(
            OperationCode='SigmaSnapCommand',
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[])
        return self.send(ptp, payload)

    def get_big_partial_pict_file(self, store_address, start_address, max_length):
        ptp = Container(
            OperationCode='SigmaGetBigPartialPictFile',
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[store_address, start_address, max_length])
        response = self.recv(ptp)
        return self._parse_if_data(response, _BigPartialPictFile)
