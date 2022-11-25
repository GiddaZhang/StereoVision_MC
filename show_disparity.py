import cv2
import numpy as np

from stereovision.stereo_cameras import StereoPair
from stereovision_new.blockmatchers import StereoBM, StereoSGBM
from stereovision_new.calibration import StereoCalibration
from stereovision_new.ui_utils import find_files, BMTuner, STEREO_BM_FLAG

def show_disparity(pair, calibration, block_matcher, base_len, focal_len):

    # 鼠标召回事件，打印点击处深度值
    def onMouse(event, x, y, flags, param):
        if event == cv2.EVENT_FLAG_LBUTTON:
            print('depth: {}mm'.format(param[y-1][x-1]))

    image_pair = pair.get_frames()
    rectified_pair = calibration.rectify(image_pair)
    disparity = block_matcher.get_disparity(rectified_pair)

    depth_map = base_len * focal_len / disparity
    disparity_norm = disparity / disparity.max()

    cv2.imshow('Left camera', rectified_pair[0])
    cv2.imshow('Right camera', rectified_pair[1])
    cv2.waitKey(1)
    cv2.imshow('disparity', disparity_norm)
    cv2.waitKey(1)
    cv2.setMouseCallback('disparity', onMouse, depth_map)

def main():
    # 修改此处指定摄像头序号
    left_cam = 1
    right_cam = 2

    # 标定参数，修改此处指定路径
    calibration_folder = 'calibrate/1/'
    calibration = StereoCalibration(input_folder=calibration_folder)
    block_matcher = StereoSGBM()

    with StereoPair(devices=(left_cam, right_cam)) as pair:
        
        focal_len = pair.get_focal_length('calibrate/1/cam_mats_left.npy', 
                                          'calibrate/1/cam_mats_right.npy')
        base_len = 57       # 57mm基线

        while True:
            
            show_disparity(pair, calibration, block_matcher, base_len, focal_len)

if __name__ == "__main__":
    main()