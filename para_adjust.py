import cv2
from stereovision.calibration import StereoCalibration
from stereovision.ui_utils import find_files

def main():

    num = 0
    block_size = 0
    calibration_folder = 'calibrate/2'
    image_folder = 'pics'

    calibration = StereoCalibration(input_folder=calibration_folder)
    input_files = find_files(image_folder)
    image_pair = [cv2.imread(image) for image in input_files[:2]]
    input_files = input_files[2:]
    rectified_pair = calibration.rectify(image_pair)

    cv2.imshow('original', rectified_pair[0])
    cv2.namedWindow('SGBM')
    cv2.createTrackbar('num', 'SGBM', 2, 10, lambda x: None)
    cv2.createTrackbar('blockSize', 'SGBM', 5, 255, lambda x: None)

    while True:
        num = cv2.getTrackbarPos('num', 'SGBM')
        block_size = cv2.getTrackbarPos('blockSize', 'SGBM')
        if block_size % 2 == 0:
            block_size += 1
        block_size = max(block_size, 5)
        num = max(1, num)

        stereo = cv2.StereoSGBM_create(minDisparity=0, numDisparities=16*num, blockSize=block_size)
        disparity = stereo.compute(rectified_pair[0], rectified_pair[1])
        disparity = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        disparity = cv2.applyColorMap(disparity, 2)
        cv2.imshow('SGBM', disparity)

        cv2.waitKey(1000)

if __name__ == '__main__':
    main()