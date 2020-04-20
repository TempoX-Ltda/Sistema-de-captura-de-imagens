import cv2
from pathlib import Path
from threading import Thread, Lock
from configparser import ConfigParser
import time
import timeit
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

class getVelocity():

    def __init__(self, CameraConfigPath, paternName):
        print(CameraConfigPath)
        print(paternName)
        self.CameraConfigPath = CameraConfigPath
        self.paternName       = paternName

        self.EncoderConfig = ConfigParser()
        self.EncoderConfig.read(Path(self.CameraConfigPath))
        print('Arquivo de configurações da Câmera para configurações do Encoder foi carregado: ' + str(self.CameraConfigPath))
        
        self.encoderXYpos    = eval(self.EncoderConfig.get(self.paternName, 'encoderXYpos'))
        self.showEncoderPos  = bool(self.EncoderConfig.get(self.paternName, 'showEncoderPos'))
        self.encodeStripSize = float(self.EncoderConfig.get(self.paternName, 'encodeStripSize')) # Em milímetros
        
        for encoder in range(len(self.encoderXYpos)):
            print('A posição do encoder ' + str(encoder) + " é: " + str(self.encoderXYpos[encoder]))
        
        self.EncoderColors = []
        self.velocity = 0.0

        self.threadLock = Lock()
        self.stopped    = False
        self.newColor   = False


    def start(self):
        Thread(target=self.measure, args=()).start()
        return self

    def measure(self):
        
        lastAtt = timeit.default_timer()
        lastColor = [LabColor(lab_l=0.9, lab_a=16.3, lab_b=-2.22)]
        _EncoderColors = []

        while self.stopped == False:
            with self.threadLock:
                newcolor = self.newColor

            if newcolor == True:
                #print('NewColor is True')

                _EncoderColors = []
                for color in self.EncoderColors:
                    color_RGB = sRGBColor(color[0], color[1], color[2])
                    _EncoderColors.append(convert_color(color_RGB, LabColor))

                with self.threadLock:
                    try:
                        difference = delta_e_cie2000(_EncoderColors[0], lastColor[0])
                    
                        if difference > 10:
                            print(difference)
                            lastColor = _EncoderColors
                    except:
                        pass
                with self.threadLock:
                    self.newColor = False

    def stop(self):
        print('"getVelocity" will be stopped')
        self.stopped = True

    def get(self):
        'Retorna a velocidade com que a esteira está se movendo'
        
        return self.velocity
    
    def sendEncoderColors(self, EncoderColors):
        self.EncoderColors = EncoderColors
        with self.threadLock:
            self.newColor = True
            #print('Change NewColor to True')
            #print(self.newColor)