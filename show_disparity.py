import cv2
import time
# from YOLO.yolo import yolo
from stereovision.stereo_cameras import StereoPair
from stereovision.blockmatchers import StereoBM, StereoSGBM
from stereovision.calibration import StereoCalibration
from stereovision.ui_utils import find_files, BMTuner, STEREO_BM_FLAG

dis = []
draw = False
X, Y, d = None, None, None
h = 10
def show_disparity(pair, calibration, block_matcher, base_len, focal_len, detector):
    start = time.time()
    m_len = 3
    # 鼠标召回事件，打印点击处深度值
    def onMouse(event, x, y, flags, param):
        if event == cv2.EVENT_FLAG_LBUTTON:
            global draw, X, Y, d
            draw = True
            print('depth: {}mm'.format(param[y-1][x-1]))
            X, Y = x, y
            d = param[y-1][x-1]

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
    # disparity = cv2.bilateralFilter(disparity, d=0, sigmaColor=150, sigmaSpace=15)
    disparity = cv2.medianBlur(disparity, 5)
    disparity = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    disparity = cv2.applyColorMap(disparity, 2)

    end = time.time()
    seconds = end - start  # 处理一帧所用的时间
    fps = round(1 / seconds, 2)  # 一秒钟可以处理多少帧
    fps = str(fps) +' fps'
    cv2.putText(disparity, fps, (310,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
    cv2.imshow('disparity', disparity)
    cv2.moveWindow('disparity', 0, 0)
    cv2.waitKey(1)
    if draw:
        rectified_pair[0] = cv2.rectangle(
            rectified_pair[0], (X-h, Y-h), (X+h, Y+h), (0, 0, 255), 2)
        cv2.putText(rectified_pair[0], str(round(d, 2)), (X-h,Y-h), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    cv2.imshow('original', rectified_pair[0])
    cv2.moveWindow('original', 640, 0)
    cv2.waitKey(1)
    cv2.setMouseCallback('disparity', onMouse, depth_map)

def main():
    # 修改此处指定摄像头序号
    left_cam = 1
    right_cam = 2

    # 标定参数，修改此处指定路径
    calibration_folder = 'calibrate/3/'
    calibration = StereoCalibration(input_folder=calibration_folder)
    block_matcher = StereoSGBM(min_disparity=0, num_disp=64, sad_window_size=3)
    # block_matcher = StereoSGBM()

    # 初始化检测器1
    # Yolo = yolo('YOLO\yolov3.txt',
    #             'YOLO\yolov3.weights',
    #             'YOLO\yolov3.cfg')

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