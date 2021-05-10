from sigma_ptpy import SigmaPTPy
from sigma_ptpy.schema import CamDataGroup3, SnapCommand
from sigma_ptpy.enum import DestToSave, CaptStatus
import cv2
import numpy as np


if __name__ == '__main__':
    camera = SigmaPTPy()

    with camera.session():
        camera.config_api()
        camera.set_cam_data_group3(CamDataGroup3(DestToSave=DestToSave.InComputer))
        camera.snap_command(SnapCommand())  # Start shooting

        # Wait to complete shooting
        while True:
            status = camera.get_cam_capt_status()
            if status.CaptStatus in [CaptStatus.ImageGenCompleted, CaptStatus.ImageDataStorageCompleted]:
                break
            elif status.CaptStatus in [CaptStatus.ShootInProgress, CaptStatus.ShootSuccess,
                                       CaptStatus.ImageGenInProgress, CaptStatus.AFSuccess,
                                       CaptStatus.CWBSuccess]:
                print("Waiting to complete shooting: status=%s" % status.CaptStatus)
            else:
                print("Failed shooting: status=%s" % status.CaptStatus)
                exit(1)

        # Save a picture.
        info = camera.get_pict_file_info2()
        pict = camera.get_big_partial_pict_file(info.FileAddress, 0, info.FileSize)
        img = cv2.imdecode(np.frombuffer(pict.PartialData, np.uint8), cv2.IMREAD_COLOR)
        filename = info.FileName.decode("utf8")
        cv2.imwrite(filename, img)
        print("A picture is saved as %s." % filename)
