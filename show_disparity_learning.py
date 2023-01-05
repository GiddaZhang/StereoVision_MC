import cv2

from stereovision.stereo_cameras import StereoPair
from stereovision.calibration import StereoCalibration
from PSMNet.PSMNet import PSMNet

def show_disparity(pair, calibration, block_matcher, base_len, focal_len, detector):

    m_len = 1
    # 鼠标召回事件，打印点击处深度值
    def onMouse(event, x, y, flags, param):
        if event == cv2.EVENT_FLAG_LBUTTON:
            print('depth: {}mm'.format(param[y-1][x-1]))

    image_pair = pair.get_frames()
    rectified_pair = calibration.rectify(image_pair)
    disparity = block_matcher.get_disparity(rectified_pair)

    # dis.append(disparity)
    # if len(dis) > m_len:
    #     del dis[0]
    # for i in range(len(dis) - 1):
    #     disparity += dis[i]
    # disparity /= len(dis)
    # depth_map = base_len * focal_len / disparity
    # disparity = cv2.bilateralFilter(disparity, d=0, sigmaColor=150, sigmaSpace=15)
    # disparity = cv2.medianBlur(disparity, 5)
    # disparity = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    # disparity = cv2.applyColorMap(disparity, 2)

    cv2.imshow('disparity', disparity)
    cv2.waitKey(1)
    cv2.imshow('original', rectified_pair[0])
    cv2.moveWindow('original', 640, 0)
    cv2.waitKey(1)
    # cv2.setMouseCallback('disparity', onMouse, depth_map)

def main():
    # 修改此处指定摄像头序号
    left_cam = 1
    right_cam = 2

    # 标定参数，修改此处指定路径
    calibration_folder = 'calibrate/3/'
    calibration = StereoCalibration(input_folder=calibration_folder)
    block_matcher = PSMNet()
    # block_matcher = StereoSGBM()

    with StereoPair(devices=(left_cam, right_cam)) as pair:
        
        focal_len = pair.get_focal_length('calibrate/3/cam_mats_left.npy', 
                                          'calibrate/3/cam_mats_right.npy')
        base_len = 56.1       # 57mm基线

        while True:

            show_disparity(pair, 
                        calibration, 
                        block_matcher, 
                        base_len, 
                        focal_len,
                        None
                        )

if __name__ == "__main__":
    main()