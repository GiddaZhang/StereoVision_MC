import cv2
import numpy

class cascade_detector(object):

    def __init__(self, path):
        # 加载猫脸检测器
        self.face_cascade = cv2.CascadeClassifier(path)
    
    def predict(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.02,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
        ) 
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(img,'Cat',(x,y-7), 3, 1.2, (0, 255, 0), 2, cv2.LINE_AA)
        
        return img