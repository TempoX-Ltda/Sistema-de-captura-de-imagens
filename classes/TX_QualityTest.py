import cv2
from pathlib import Path
from threading import Thread, Lock

class QualityTest():

    def __init__(self, baseImgPath, imgToFind):
        print(baseImgPath)
        self.baseImg = cv2.imread(baseImgPath)
        self.imgToFind = imgToFind
        self.threadLock = Lock()
        
        self.stopped = False
    def start(self):
        Thread(target=self.findPartsOnBaseImg, args=()).start()
        return self

    def findPartsOnBaseImg(self):
        pass
        '''
        while self.stopped is False:
            print(self.imgToFind)
        '''
        
    def stop(self):
        print('"findPartsOnBaseImg" will be stopped')
        self.stopped = True