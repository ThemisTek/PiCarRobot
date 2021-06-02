import cv2
import numpy as np
import time
import logging
from vlogging import VisualRecord


class ImageSaver :
    def __init__(self,cap):
        self.width = 320
        self.height = 200
        self.cap = cap
        self.image = np.empty((self.width,self.height,3))
        self.FolderName = "cameraLogs" + time.strftime("%Y%m%d-%H%M%S")
        self.logger = logging.getLogger('./' + self.FolderName +'/logs.txt')
        fh = logging.FileHandler(self.FolderName + '.html',mode = "w")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(fh)
        self.i = 0
    
    def Start(self):
        while True:
            self.image = self.cap.read()[1]
            self.log()
            self.i +=1
            cv2.imshow("Threshold lower image", self.image)
            l = cv2.waitKey(5) & 0XFF
            if(l == ord('q')):
                self.cap.release()
                break
    
    def log(self):
        logText = "log"
        self.logger.info(VisualRecord(logText,self.image,str(self.i)))


cap = cv2.VideoCapture(0)

saver = ImageSaver(cap)
saver.Start()