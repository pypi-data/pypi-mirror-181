import time

import torch
import numpy as np
from torchvision import models, transforms
from torch.autograd import Variable
import cv2
from PIL import Image


class classifier():
    def __init__(self,model,classes) :
        device=torch.device('cpu')
        self.preprocess = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        self.model=torch.load(model,map_location=device)
        self.classes=classes

    def run(self,image):
        image = image[:, :, [2, 1, 0]]
        test_image_tensor = self.preprocess(image)
        test_image_tensor = test_image_tensor
        test_image_tensor = Variable(torch.unsqueeze(test_image_tensor, dim=0).float(), requires_grad=False)
        with torch.no_grad():
            self.model.eval()
            out = self.model(test_image_tensor)
            ps = torch.exp(out) 
            ps = ps / torch.sum(ps)
            topk, topclass = ps.topk(1, dim=1)
            return(self.classes[topclass.cpu().numpy()[0][0]], topk.cpu().numpy()[0][0])

if __name__=="__main__":
    device=torch.device('cpu')
    classes=['cat','dog']
    cap = cv2.VideoCapture(0)
    cls=classifier(r'C:\Users\Administrator\Desktop\Classification_Model.pth',classes)
    with torch.no_grad():
        while True:
            ret, image = cap.read()
            label, score = cls.run(image)
            print(label,score)



  