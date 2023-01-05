from stereovision.stereo_cameras import StereoPair
from stereovision.blockmatchers import StereoBM, StereoSGBM
from stereovision.calibration import StereoCalibration
from stereovision.ui_utils import find_files, BMTuner, STEREO_BM_FLAG
import os
import time
import cv2
import numpy as np

dis = []


def show_disparity(pair, calibration, block_matcher, base_len, focal_len, detector):

    m_len = 2

    image_pair = pair.get_frames()
    rectified_pair = calibration.rectify(image_pair)
    disparity = block_matcher.get_disparity(rectified_pair)

    dis.append(disparity)
    if len(dis) > m_len:
        del dis[0]
    for i in range(len(dis) - 1):
        disparity += dis[i]
    disparity /= len(dis)
    depth_map = base_len * focal_len / disparity
    print(base_len * focal_len )
    # disparity = cv2.bilateralFilter(disparity, d=0, sigmaColor=150, sigmaSpace=15)
    disparity = cv2.medianBlur(disparity, 5)
    disparity_ = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    disparity_ = cv2.applyColorMap(disparity_, 2)

    cv2.imshow('disparity', disparity_)
    cv2.waitKey(1)
    cv2.imshow('original', rectified_pair[0])
    cv2.moveWindow('original', 640, 0)
    cv2.waitKey(1)

    return rectified_pair[0], disparity

def main():
    """
    Show the video from two webcams successively.
    """

    # 修改此处指定摄像头序号
    lcam = 1
    rcam = 2
    capture_pic = True

    calibration_folder = 'calibrate/3/'
    calibration = StereoCalibration(input_folder=calibration_folder)
    block_matcher = StereoSGBM(min_disparity=0, num_disp=64, sad_window_size=3)
    base_len = 56.1       # 57mm基线

    with StereoPair(devices=(lcam, rcam)) as pair:
        focal_len = pair.get_focal_length('calibrate/3/cam_mats_left.npy',
                                          'calibrate/3/cam_mats_right.npy')
        if not capture_pic:
            pair.show_videos()

        else:
            interval = 30       # 时间间隔
            output_folder = 'RGBD'
            i = 1
            while True:
                start = time.time()
                while time.time() < start + interval:
                    l, d = show_disparity(pair,
                                   calibration,
                                   block_matcher,
                                   base_len,
                                   focal_len,
                                   None
                                   )
                
                filename_1 = "{}.png".format(i)
                filename_2 = "{}.npy".format(i)
                output_path_1 = os.path.join(output_folder, filename_1)
                output_path_2 = os.path.join(output_folder, filename_2)
                cv2.imwrite(output_path_1, l)
                np.save(output_path_2, d)
                i += 1

if __name__ == "__main__":
    main()
