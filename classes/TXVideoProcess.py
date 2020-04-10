from configparser import ConfigParser
import imutils
import cv2
from pathlib import Path

class VideoTresh():
    'Faz o recorte das peças do frame de acordo com o método especificado, retornando os contornos das peças e uma img binária com Tresh aplicado'

    def __init__(self, ColorConfigPath):
        self.ColorConfig = ConfigParser()
        self.ColorConfig.read(Path(ColorConfigPath))
        print('Arquivo de configurações de cor/padrão foi carregado: ' + str(ColorConfigPath))
        self.paternSelected = False
        
    def selectPatern(self , patern):
        'Selecione como "Patern" o nome da seção do arquivo .ini que você passou ao instânciar VideoTresh.'
        self.blur = tuple(eval(self.ColorConfig.get(patern, 'blur')))
        self.convertcolorMode = str(self.ColorConfig.get(patern, 'convertcolorMode'))
        self.erodeIterations = int(self.ColorConfig.get(patern, 'erodeIterations'))
        self.dilateIterations = int(self.ColorConfig.get(patern, 'dilateIterations'))
        self.tresholdTresh = int(self.ColorConfig.get(patern, 'tresholdTresh'))
        self.tresholdMaxVal = int(self.ColorConfig.get(patern, 'tresholdMaxVal'))
        self.tresholdType = str(self.ColorConfig.get(patern, 'tresholdType'))
        self.findContoursMode = str(self.ColorConfig.get(patern, 'findContoursMode'))
        self.findContoursMetod = str(self.ColorConfig.get(patern, 'findContoursMetod'))
        
        self.paternSelected = True

    def getPartsContours(self, img):
        if self.paternSelected == True:
            'Passe como "img" uma numpy array, esse função irá retornar o contorno dos objetos que estiverem na "img" e que estejam de acordo com os parâmetros especificados no arquivo que foi passado ao chamar "selectPatern", o retorno terá o formato (contours, tresh)'
            blurred = cv2.blur(img, self.blur)
            colorConverted = cv2.cvtColor(blurred, getattr(cv2, self.convertcolorMode))
            eroded = cv2.erode(colorConverted, None, iterations=self.erodeIterations)
            dilated = cv2.dilate(eroded, None, iterations=self.dilateIterations)
            tresh = cv2.threshold(dilated, self.tresholdTresh, self.tresholdMaxVal, getattr(cv2, self.tresholdType))[1]
            (contours, lx) = cv2.findContours(tresh.copy(), getattr(cv2, self.findContoursMode), getattr(cv2, self.findContoursMetod))
            return (contours, tresh)
        else:
            print('Antes de executar "getPartsContours" você deve utilizar "selectPatern" para especificar qual a seção do arquivo de configurações você deseja utilizar!')
            exit()

'''
    def tresh_bt_cae(self, img): #Padrão BURITI CAEMMUN
        suave = cv2.blur(img, (5,5))
        hsv = cv2.cvtColor(suave,cv2.COLOR_BGR2HSV)
        eroded = cv2.erode(hsv, None, iterations=5)
        dilated = cv2.dilate(eroded, None, iterations=5)
        thresh_hsv = cv2.inRange(dilated, (10, 30, 132), (26, 77, 176)) #[ 10  30 132] [ 26 77 176]
        (contours, lx) = cv2.findContours(thresh_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return (contours, thresh_hsv)

    def tresh_bf_cae(self, img): #Padrão BRANCO FOSCO CAEMMUN
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        suave = cv2.blur(gray, (3,3))
        eroded = cv2.erode(suave, None, iterations=5)
        dilated = cv2.dilate(eroded, None, iterations=5)
        thresh = cv2.threshold(dilated, 190, 255, cv2.THRESH_BINARY)[1]
        (contours, lx) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return (contours, thresh)

    def tresh_esteira_branco(self, img): #Padrão Branco teste esteira
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        suave = cv2.blur(gray, (3,3))
        eroded = cv2.erode(suave, None, iterations=5)
        dilated = cv2.dilate(eroded, None, iterations=5)
        thresh = cv2.threshold(dilated, 190, 255, cv2.THRESH_BINARY)[1]
        (contours) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return (contours, thresh)
'''
class VideoAlign(object):
    'Possui métodos que são utilizados para alinhar o video recebido pela câmera ou arquivo de vídeo.'
    def __init__(self, CameraConfigPath):
        self.CameraConfig = ConfigParser()
        self.CameraConfig.read(Path(CameraConfigPath))
        print('Arquivo de configurações da Câmera foi carregado: ' + str(CameraConfigPath))
        self.start_scan   = 0
        self.end_scan     = 0
        self.scanlineYpos = 0
    
    def selectPatern(self, patern):
        'Selecione como "Patern" o nome da seção do arquivo .ini que você passou ao instânciar VideoAlign.'
        
        self.resizedShape = tuple(eval(self.CameraConfig.get(patern, 'resizedShape')))
        self.recortY      = eval(self.CameraConfig.get(patern, 'recortY'))
        self.recortX      = eval(self.CameraConfig.get(patern, 'recortX'))
        self.rotateAngle  = float(self.CameraConfig.get(patern, 'rotateAngle'))
        self.start_scan   = int(self.CameraConfig.get(patern, 'scanlineStart'))
        self.end_scan     = int(self.CameraConfig.get(patern, 'scanlineEnd'))
        self.scanlineYpos = int(self.CameraConfig.get(patern, 'scanlineYPos'))

    def AlignFrame(self, img):
        resized = cv2.resize(img, self.resizedShape)
        recort = resized[self.recortY[0]:self.recortY[1], 
                         self.recortX[0]:self.recortX[1]]
        return imutils.rotate_bound(recort, self.rotateAngle)