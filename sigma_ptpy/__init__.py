import logging
import sys
import os
from rainbow_logging_handler import RainbowLoggingHandler
from .sigma_ptpy import SigmaPTPy

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

__all__ = (
    'SigmaPTPy'
)
