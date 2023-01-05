from __future__ import print_function
import argparse
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torch.nn.functional as F
import time
from PSMNet.models import *
from PIL import Image

class PSMNet(object):
    
    def __init__(self):
        normal_mean_var = {'mean': [0.485, 0.456, 0.406],
                           'std': [0.229, 0.224, 0.225]}
        self.infer_transform = transforms.Compose([transforms.ToTensor(),
                                                   transforms.Normalize(**normal_mean_var)])
        self.model = stackhourglass(192)
        self.model = nn.DataParallel(self.model, device_ids=[0])
        self.model.cuda()
        print('load PSMNet')
        state_dict = torch.load('PSMNet/pretrained_sceneflow_new.tar')
        self.model.load_state_dict(state_dict['state_dict'])
        print('Number of model parameters: {}'.format(sum([p.data.nelement() for p in self. model.parameters()])))
    
    def get_disparity(self, img_pair):

        def test(imgL,imgR):
            self.model.eval()

            imgL = imgL.cuda()
            imgR = imgR.cuda()     

            with torch.no_grad():
                disp = self.model(imgL,imgR)

            disp = torch.squeeze(disp)
            pred_disp = disp.data.cpu().numpy()

            return pred_disp
            
        imgL = self.infer_transform(img_pair[0])
        imgR = self.infer_transform(img_pair[1])
        # pad to width and hight to 16 times
        if imgL.shape[1] % 16 != 0:
            times = imgL.shape[1]//16
            top_pad = (times+1)*16 - imgL.shape[1]
        else:
            top_pad = 0

        if imgL.shape[2] % 16 != 0:
            times = imgL.shape[2]//16
            right_pad = (times+1)*16-imgL.shape[2]
        else:
            right_pad = 0

        imgL = F.pad(imgL, (0, right_pad, top_pad, 0)).unsqueeze(0)
        imgR = F.pad(imgR, (0, right_pad, top_pad, 0)).unsqueeze(0)

        pred_disp = test(imgL,imgR)

        if top_pad !=0 and right_pad != 0:
            img = pred_disp[top_pad:,:-right_pad]
        elif top_pad ==0 and right_pad != 0:
            img = pred_disp[:,:-right_pad]
        elif top_pad !=0 and right_pad == 0:
            img = pred_disp[top_pad:,:]
        else:
            img = pred_disp
        
        img = (img*256).astype('uint16')
        
        return img
