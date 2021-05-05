import logging
from ptpy import USB
from construct import Container
from .ptp import SigmaPTP
from rainbow_logging_handler import RainbowLoggingHandler
import sys

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
