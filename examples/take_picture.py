from sigma_ptpy import SigmaPTPy
from sigma_ptpy.schema import CamDataGroup2, CamDataGroup3, CamDataGroupFocus, SnapCommand
from sigma_ptpy.enum import CaptStatus, DestToSave, ExposureMode, FocusMode
import time


def wait_completion(camera, image_id):
    for _ in range(10):
        status = camera.get_cam_capt_status(image_id)
        if status.CaptStatus in [CaptStatus.ImageGenCompleted, CaptStatus.ImageDataStorageCompleted]:
            return status
        elif status.CaptStatus in [CaptStatus.ShootInProgress, CaptStatus.ShootSuccess,
                                   CaptStatus.ImageGenInProgress, CaptStatus.AFSuccess,
                                   CaptStatus.CWBSuccess]:
            print("Waiting to complete shooting: status=%s" % status.CaptStatus)
            time.sleep(1)
        else:
            print("Failed shooting: status=%s" % status.CaptStatus)
            break


if __name__ == '__main__':
    camera = SigmaPTPy()

    with camera.session():
        camera.config_api()

        camera.set_cam_data_group_focus(CamDataGroupFocus(FocusMode=FocusMode.AF_S))
        camera.set_cam_data_group2(CamDataGroup2(ExposureMode=ExposureMode.Manual))
        camera.set_cam_data_group3(CamDataGroup3(DestToSave=DestToSave.InComputer))

        camera.snap_command(SnapCommand())  # Start shooting

        # Wait to complete shooting
        status = wait_completion(camera, 0)
        if status:
            print(status)
            # Save a picture.
            info = camera.get_pict_file_info2()
            print(info)
            pict = camera.get_big_partial_pict_file(info.FileAddress, 0, info.FileSize)
            filename = info.FileName.decode("utf8")
            with open(filename, "wb") as fout:
                fout.write(pict.PartialData)
                print("A picture is saved as %s." % filename)

            camera.clear_image_db_single(status.ImageId)

        camera.close_application()
