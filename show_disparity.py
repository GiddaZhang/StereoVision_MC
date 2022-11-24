import os
import time
import cv2
from stereovision.stereo_cameras import StereoPair
from stereovision_new.blockmatchers import StereoBM, StereoSGBM
from stereovision_new.calibration import StereoCalibration
from stereovision_new.ui_utils import find_files, BMTuner, STEREO_BM_FLAG

def main():
    # 修改此处指定摄像头序号
    left_cam = 1
    right_cam = 2

    # 标定参数，修改此处指定路径
    calibration_folder = 'calibrate/1/'
    calibration = StereoCalibration(input_folder=calibration_folder)
    block_matcher = StereoSGBM()

    with StereoPair(devices=(left_cam, right_cam)) as pair:
        
        while True:
            image_pair = pair.get_frames()
            rectified_pair = calibration.rectify(image_pair)

            disparity = block_matcher.get_disparity(rectified_pair)
            norm_coeff = 255 / disparity.max()

            cv2.imshow('disparity', disparity * norm_coeff / 255)
            cv2.imshow('image', image_pair[1])
            cv2.waitKey(1)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__ == "__main__":
    main()