from ptpy import PTP
from construct import (
    Adapter, Array, BitsInteger, Bitwise, Bytes, Container, Default, Int16sb,
    Int16sl, Int16sn, Int16ub, Int16ul, Int16un, Int32sb, Int32sl, Int32sn,
    Int32ub, Int32ul, Int32un, Int64sb, Int64sl, Int64sn, Int64ub, Int64ul,
    Int64un, Int8sb, Int8sl, Int8sn, Int8ub, Int8ul, Int8un, Pass, Padding,
    PrefixedArray, Struct, Switch, If, String, CString, GreedyBytes, Mapping
)

class SigmaPTP(PTP):

    def __init__(self, *args, **kwargs):
        super(SigmaPTP, self).__init__(*args, **kwargs)

    def _OperationCode(self, **vendor_operations):
        return super(SigmaPTP, self)._OperationCode(
            SigmaGetCamDataGroup1=0x9012,
            SigmaGetCamDataGroup2=0x9013,
            SigmaGetCamDataGroup3=0x9014,
            SigmaGetCamCaptStatus=0x9015,
            SigmaSetCamDataGroup1=0x9016,
            SigmaSetCamDataGroup2=0x9017,
            SigmaSetCamDataGroup3=0x9018,
            SigmaSnapCommand=0x901B,
            SigmaGetBigPartialPictFile=0x9022,
            SigmaGetViewFrame=0x902B,
            SigmaGetPictFileInfo2=0x902D,
            SigmaConfigApi=0x9035,
            **vendor_operations
        )

    def _ResponseCode(self, **vendor_operations):
        return super(SigmaPTP, self)._ResponseCode(
            SigmaGetCamDataGroup1=0x9012,
            SigmaGetCamDataGroup2=0x9013,
            SigmaGetCamDataGroup3=0x9014,
            SigmaGetCamCaptStatus=0x9015,
            SigmaSetCamDataGroup1=0x9016,
            SigmaSetCamDataGroup2=0x9017,
            SigmaSetCamDataGroup3=0x9018,
            SigmaSnapCommand=0x901B,
            SigmaGetBigPartialPictFile=0x9022,
            SigmaGetViewFrame=0x902B,
            SigmaGetPictFileInfo2=0x902D,
            SigmaConfigApi=0x9035,
            **vendor_operations
        )
