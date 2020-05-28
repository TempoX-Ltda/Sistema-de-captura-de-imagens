from configparser import ConfigParser
import imutils
import cv2
from pathlib import Path

class VideoTresh():
    'Faz o recorte das peças do frame de acordo com o método especificado, retornando os contornos das peças e uma img binária com Tresh aplicado'

    def __init__(self, ColorConfigPath):
        self.ColorConfigPath = Path(ColorConfigPath)
        if not self.ColorConfigPath.exists():
            print('O arquivo não pode ser carregado: ' + str(self.ColorConfigPath))
            exit()
        self.ColorConfig = ConfigParser()
        self.ColorConfig.read(self.ColorConfigPath)
        print('Arquivo de configurações de cor/padrão foi carregado: ' + str(ColorConfigPath))
        
        self.perfectPaternPath = ''
        self.paternSelected = False

    def selectPatern(self , patern):
        'Selecione como "Patern" o nome da seção do arquivo .ini que você passou ao instânciar VideoTresh.'
        self.colorType = str(self.ColorConfig.get(patern, 'colorType'))

        if self.colorType == 'solid':
            self.blur              = tuple(eval(self.ColorConfig.get(patern, 'blur')))
            self.convertcolorMode  = str(self.ColorConfig.get(patern, 'convertcolorMode'))
            self.erodeIterations   = int(self.ColorConfig.get(patern, 'erodeIterations'))
            self.dilateIterations  = int(self.ColorConfig.get(patern, 'dilateIterations'))
            self.tresholdTresh     = int(self.ColorConfig.get(patern, 'tresholdTresh'))
            self.tresholdMaxVal    = int(self.ColorConfig.get(patern, 'tresholdMaxVal'))
            self.tresholdType      = str(self.ColorConfig.get(patern, 'tresholdType'))
            self.findContoursMode  = str(self.ColorConfig.get(patern, 'findContoursMode'))
            self.findContoursMetod = str(self.ColorConfig.get(patern, 'findContoursMetod'))
        
        elif self.colorType == 'veined':
            self.blur              = tuple(eval(self.ColorConfig.get(patern, 'blur')))
            self.convertcolorMode  = str(self.ColorConfig.get(patern, 'convertcolorMode'))
            self.erodeIterations   = int(self.ColorConfig.get(patern, 'erodeIterations'))
            self.dilateIterations  = int(self.ColorConfig.get(patern, 'dilateIterations'))
            self.colorLowerRange   = tuple(eval(self.ColorConfig.get(patern, 'colorLowerRange')))
            self.colorUpperRange   = tuple(eval(self.ColorConfig.get(patern, 'colorUpperRange')))
            self.findContoursMode  = str(self.ColorConfig.get(patern, 'findContoursMode'))
            self.findContoursMetod = str(self.ColorConfig.get(patern, 'findContoursMetod'))
        else:
            print('Não foi especificado corretamente o colorType!')
            exit()

        self.perfectPaternPath = self.ColorConfig.get(patern, 'perfectPatern')
        self.paternSelected = True

    def getPartsContours(self, img):
        'Passe como "img" uma numpy array, esse função irá retornar o contorno dos objetos que estiverem na "img" e que estejam de acordo com os parâmetros especificados no arquivo que foi passado ao chamar "selectPatern", o retorno terá o formato (contours, tresh)'
        
        if self.paternSelected == True:

            if self.colorType == 'solid':
                blurred        = cv2.blur(img, self.blur)
                colorConverted = cv2.cvtColor(blurred, getattr(cv2, self.convertcolorMode))
                eroded         = cv2.erode(colorConverted, None, iterations=self.erodeIterations)
                dilated        = cv2.dilate(eroded, None, iterations=self.dilateIterations)
                tresh          = cv2.threshold(dilated, self.tresholdTresh, self.tresholdMaxVal, getattr(cv2, self.tresholdType))[1]
                (contours, lx) = cv2.findContours(tresh.copy(), getattr(cv2, self.findContoursMode), getattr(cv2, self.findContoursMetod))
                return (contours, tresh)
            
            elif self.colorType == 'veined':
                
                blurred        = cv2.blur(img, self.blur)
                colorConverted = cv2.cvtColor(blurred, getattr(cv2, self.convertcolorMode))
                eroded         = cv2.erode(colorConverted, None, iterations=self.erodeIterations)
                dilated        = cv2.dilate(eroded, None, iterations=self.dilateIterations)
                inrange        = cv2.inRange(dilated, self.colorLowerRange, self.colorUpperRange) #[ 10  30 132] [ 26 77 176]
                (contours, lx) = cv2.findContours(inrange.copy(), getattr(cv2, self.findContoursMode), getattr(cv2, self.findContoursMetod))
                return (contours, inrange)
            else:
                print('Não foi especificado corretamente o colorType!')
                exit()
        else:
            print('Antes de executar "getPartsContours" você deve utilizar "selectPatern" para especificar qual a seção do arquivo de configurações você deseja utilizar!')
            exit()

class VideoAlign(object):
    'Possui métodos que são utilizados para alinhar o video recebido pela câmera ou arquivo de vídeo.'
    def __init__(self, CameraConfigPath):
        self.CameraConfig = ConfigParser()
        self.CameraConfigPath = Path(CameraConfigPath)
        if not self.CameraConfigPath.exists():
            print('O arquivo não pode ser carregado: ' + str(self.CameraConfigPath))
            exit()

        self.CameraConfig.read(self.CameraConfigPath)
        print('Arquivo de configurações da Câmera foi carregado: ' + str(self.CameraConfigPath))
        self.start_scan         = 0
        self.end_scan           = 0
        self.scanlineYpos       = 0

        self.paternName = ''
        self.mmByPx = 0
        
    def selectPatern(self, patern):
        'Selecione como "Patern" o nome da seção do arquivo .ini que você passou ao instânciar VideoAlign.'
        self.paternName = patern

        self.resizedShape       = tuple(eval(self.CameraConfig.get(self.paternName, 'resizedShape')))
        self.recortY            = eval(self.CameraConfig.get(self.paternName, 'recortY'))
        self.recortX            = eval(self.CameraConfig.get(self.paternName, 'recortX'))
        self.rotateAngle        = float(self.CameraConfig.get(self.paternName, 'rotateAngle'))
        self.start_scan         = int(self.CameraConfig.get(self.paternName, 'scanlineStart'))
        self.end_scan           = int(self.CameraConfig.get(self.paternName, 'scanlineEnd'))
        self.scanlineYpos       = int(self.CameraConfig.get(self.paternName, 'scanlineYPos'))

        marksDistX              = float(self.CameraConfig.get(self.paternName, 'marksDistX'))
        marksDistY              = float(self.CameraConfig.get(self.paternName, 'marksDistY'))
        marksDistXpx            = float(self.CameraConfig.get(self.paternName, 'marksDistXpx'))
        marksDistYpx            = float(self.CameraConfig.get(self.paternName, 'marksDistYpx'))

        if (marksDistY * 1000) / marksDistYpx == (marksDistY * 1000) / marksDistYpx:
            self.mmByPx = (marksDistY * 1000) / marksDistYpx
        else:
            print('mm/px em X é diferente de mm/px em Y, finalizando programa')
            exit()

    def AlignFrame(self, img, calibrateMode=False):
        resized = cv2.resize(img, self.resizedShape)
        
        if calibrateMode == True:
            recort = resized
        elif calibrateMode == False:
            recort = resized[self.recortY[0]:self.recortY[1], 
                             self.recortX[0]:self.recortX[1]]
                        
        return imutils.rotate_bound(recort, self.rotateAngle)