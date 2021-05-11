from ptpy import PTP


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
            SigmaSetCamClockAdj=0x9019,
            SigmaSnapCommand=0x901B,
            SigmaClearImageDBSingle=0x901C,
            SigmaGetBigPartialPictFile=0x9022,
            SigmaGetCamDataGroup4=0x9023,
            SigmaSetCamDataGroup4=0x9024,
            SigmaGetCamDataGroup5=0x9027,
            SigmaSetCamDataGroup5=0x9028,
            SigmaGetLastCommandData=0x9029,
            SigmaFreeArrayMemory=0x902A,
            SigmaGetViewFrame=0x902B,
            SigmaGetPictFileInfo2=0x902D,
            SigmaCloseApplication=0x902F,
            SigmaGetCamCanSetInfo5=0x9030,
            SigmaGetCamDataGroupFocus=0x9031,
            SigmaSetCamDataGroupFocus=0x9032,
            SigmaGetCamDataGroupMovie=0x9033,
            SigmaSetCamDataGroupMovie=0x9034,
            SigmaConfigApi=0x9035,
            SigmaGetMovieFileInfo=0x9036,
            SigmaGetPartialMovieFile=0x9037,
            **vendor_operations)

    def _ResponseCode(self, **vendor_operations):
        return super(SigmaPTP, self)._ResponseCode(
            SigmaGetCamDataGroup1=0x9012,
            SigmaGetCamDataGroup2=0x9013,
            SigmaGetCamDataGroup3=0x9014,
            SigmaGetCamCaptStatus=0x9015,
            SigmaSetCamDataGroup1=0x9016,
            SigmaSetCamDataGroup2=0x9017,
            SigmaSetCamDataGroup3=0x9018,
            SigmaSetCamClockAdj=0x9019,
            SigmaSnapCommand=0x901B,
            SigmaClearImageDBSingle=0x901C,
            SigmaGetBigPartialPictFile=0x9022,
            SigmaGetCamDataGroup4=0x9023,
            SigmaSetCamDataGroup4=0x9024,
            SigmaGetCamDataGroup5=0x9027,
            SigmaSetCamDataGroup5=0x9028,
            SigmaGetLastCommandData=0x9029,
            SigmaFreeArrayMemory=0x902A,
            SigmaGetViewFrame=0x902B,
            SigmaGetPictFileInfo2=0x902D,
            SigmaCloseApplication=0x902F,
            SigmaGetCamCanSetInfo5=0x9030,
            SigmaGetCamDataGroupFocus=0x9031,
            SigmaSetCamDataGroupFocus=0x9032,
            SigmaGetCamDataGroupMovie=0x9033,
            SigmaSetCamDataGroupMovie=0x9034,
            SigmaConfigApi=0x9035,
            SigmaGetMovieFileInfo=0x9036,
            SigmaGetPartialMovieFile=0x9037,
            **vendor_operations)
