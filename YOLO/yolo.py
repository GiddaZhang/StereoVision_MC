import cv2
import numpy as np

class yolo(object):

    def __init__(self, classes, weights, config):
        
        self.scale = 0.00392
        # 加载类别
        with open(classes, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.COLORS = np.random.uniform(0, 255, size=(len(self.classes), 3))
        # 加载网络
        self.net = cv2.dnn.readNet(weights, config)   #加载模型

    def get_output_layers(self):
    
        layer_names = self.net.getLayerNames()
        try:
            output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        except:
            output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        return output_layers
    
    def draw_prediction(self, img, class_id, confidence, x, y, x_plus_w, y_plus_h):

        label = str(self.classes[class_id])
        color = self.COLORS[class_id]

        cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)  #画框，传参是左上角和右下角
        cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    def predict(self, image):

        #图像预处理
        blob = cv2.dnn.blobFromImage(image, self.scale, (416,416), (0,0,0), True, crop=False) 
        #设置输入
        self.net.setInput(blob)
        #前向传播，获取结果
        outs = self.net.forward(self.get_output_layers())

        Width = image.shape[1]
        Height = image.shape[0]
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
        output_class_ids = []
        output_confidences = []
        output_boxes = []
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
            self.draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))  #画框、标类
            
            output_class_ids.append(class_ids[i])
            output_confidences.append(confidences[i])
            output_boxes.append(boxes[i])
        
        return image
        # return output_class_ids, output_confidences, output_boxes

