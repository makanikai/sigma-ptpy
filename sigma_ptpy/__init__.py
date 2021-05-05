import cv2
import logging
import numpy as np
import sys
from construct import Container
from ptpy import USB
from rainbow_logging_handler import RainbowLoggingHandler

from .ptp import SigmaPTP

logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    '%(levelname).1s '
    '%(relativeCreated)d '
    '%(name)s'
    '[%(threadName)s:%(funcName)s:%(lineno)s] '
    '%(message)s'
)

handler = RainbowLoggingHandler(sys.stderr)
handler.setFormatter(formatter)
logger.addHandler(handler)

class SigmaPTPy(SigmaPTP, USB):

    def __init__(self, *args, **kwargs):
        logger.info("Init SigmaPTPy")
        super(SigmaPTPy, self).__init__(*args, **kwargs)

    def config_api(self):
        data = Container(
            OperationCode='SigmaConfigApi',
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[0])
        return self.recv(data)

    def get_cam_data_group1(self):
        return self._get_cam_data_group('SigmaGetCamDataGroup1', self._CamDataGroup1)

    def get_cam_data_group2(self):
        return self._get_cam_data_group('SigmaGetCamDataGroup2', self._CamDataGroup2)

    def _get_cam_data_group(self, opcode, schema):
        ptp = Container(
            OperationCode=opcode,
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[])
        response = self.recv(ptp)
        logger.debug("SigmaPTPy receives {}".format(response.Data))
        return self._parse_if_data(response, schema)

    def set_cam_data_group1(self, data):
        return self._set_cam_data_group('SigmaSetCamDataGroup1', self._CamDataGroup1, data)

    def set_cam_data_group2(self, data):
        return self._set_cam_data_group('SigmaSetCamDataGroup2', self._CamDataGroup2, data)

    def _set_cam_data_group(self, opcode, schema, data):
        payload = self._build_if_not_data(data, schema)
        logger.debug("SigmaPTPy sends {}".format(payload))
        ptp = Container(
            OperationCode=opcode,
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[])
        return self.send(ptp, payload)

    def get_view_frame(self):
        '''Load a live-view image from a camera.'''

        ptp = Container(
            OperationCode='SigmaGetViewFrame',
            SessionID=self._session,
            TransactionID=self._transaction,
            Parameter=[])
        resp = self.recv(ptp)
        jpeg = resp.Data[10:]
        return cv2.imdecode(np.fromstring(jpeg, np.uint8), cv2.IMREAD_COLOR)
