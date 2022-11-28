#############################################
# Object detection - YOLO - OpenCV
# Author : Arun Ponnusamy   (July 16, 2018)
# Website : http://www.arunponnusamy.com
############################################

#YOLO网络参数已经训练好了，直接加载现成的，可识别的类别见yolov3.txt文档，其中猫的序号为15！
#终端输出的结果：识别物体种类--物体种类对应编号--置信度--位置（左上角x，左上角y，右上角x，右上角y）
#坐标原点是图片左上角，向右为x轴正方向，向下为y轴正方向
#运行命令： python yolo_opencv.py --config yolov3.cfg --weights yolov3.weights --classes yolov3.txt --image test1.jpeg（只改这一个，输入图片）
#dog.jpg/testX.jpg都是作为输入的测试图片，object-detection.jpg是保存的输出结果（原图片+框）

import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True,
                help = 'path to input image')
ap.add_argument('-c', '--config', required=True,
                help = 'path to yolo config file')
ap.add_argument('-w', '--weights', required=True,
                help = 'path to yolo pre-trained weights')
ap.add_argument('-cl', '--classes', required=True,
                help = 'path to text file containing class names')
args = ap.parse_args()


def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)  #画框，传参是左上角和右下角

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    
image = cv2.imread(args.image)

Width = image.shape[1]
Height = image.shape[0]
scale = 0.00392

classes = None

with open(args.classes, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

net = cv2.dnn.readNet(args.weights, args.config)   #加载模型

blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)       #图像预处理

net.setInput(blob)     #设置输入

outs = net.forward(get_output_layers(net))   #前向传播，获取结果

class_ids = []     
confidences = []
boxes = []
conf_threshold = 0.5
nms_threshold = 0.4

#网络的输出为矩形框，每个矩形框由一个向量表示，所有矩形框组成一个向量组
#每个向量的长度为类别数 + 5个参数，
#这五个参数的前四个分别是矩形框在图像上的位置center_x, center_y, width, height（均为比例，范围在0-1之间），
#第五个参数是该矩形框包含一个物体的置信度。
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)    #所有类中分数最高的类
        confidence = scores[class_id]    
        if confidence > 0.5:
            center_x = int(detection[0] * Width)
            center_y = int(detection[1] * Height)
            w = int(detection[2] * Width)
            h = int(detection[3] * Height)
            x = center_x - w / 2         #左上角x
            y = center_y - h / 2         #左上角y
            class_ids.append(class_id)
            confidences.append(float(confidence))
            boxes.append([x, y, w, h])

#非极大值抑制
indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

for i in indices:
    try:
        box = boxes[i]
    except:
        i = i[0]
        box = boxes[i]
    
    x = box[0]
    y = box[1]
    w = box[2]
    h = box[3]
    draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))  #画框、标类
    print(str(classes[class_ids[i]]),class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))   #输出

cv2.imshow("object detection", image)
cv2.waitKey()
    
cv2.imwrite("object-detection.jpg", image)
cv2.destroyAllWindows()
