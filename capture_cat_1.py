import cv2

from stereovision.stereo_cameras import StereoPair
from stereovision_new.blockmatchers import StereoBM, StereoSGBM
from stereovision_new.calibration import StereoCalibration
from stereovision_new.ui_utils import find_files, BMTuner, STEREO_BM_FLAG

def show_cats(pair, calibration):
    # 加载猫脸检测器
    classPath = 'cascade/haarcascade_frontalcatface_extended.xml'
    face_cascade = cv2.CascadeClassifier(classPath)

    # 读取图片（左眼）并灰度化
    image_pair = pair.get_frames()
    rectified_pair = calibration.rectify(image_pair)
    img = rectified_pair[0]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 框出猫脸并加上文字说明
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor= 1.02,
        minNeighbors=5,
        minSize=(120, 120),
        flags=cv2.CASCADE_SCALE_IMAGE
    ) 
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.putText(img,'Cat Face',(x,y-7), 3, 1.2, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('Cat', img)
    c = cv2.waitKey(1)

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

            show_cats(pair, calibration)

if __name__ == '__main__':
    main()