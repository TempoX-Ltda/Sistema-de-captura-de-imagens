import cv2
from pathlib import Path
from configparser import ConfigParser
import timeit
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

class getVelocity():

    def __init__(self, CameraConfigPath, paternName, mode, framerate):
        print(CameraConfigPath)
        print(paternName)
        self.CameraConfigPath = CameraConfigPath
        self.paternName       = paternName
        self.mode             = mode
        self.framerate        = framerate

        print('Módulo de velocidade carregado no modo: ' + str(self.mode))
        self.EncoderConfig = ConfigParser()
        self.EncoderConfig.read(Path(self.CameraConfigPath))
        print('Arquivo de configurações da Câmera para configurações do Encoder foi carregado: ' + str(self.CameraConfigPath))
        
        self.encoderXYpos    = eval(self.EncoderConfig.get(self.paternName, 'encoderXYpos'))
        self.showEncoderPos  = bool(self.EncoderConfig.get(self.paternName, 'showEncoderPos'))
        self.encodeStripSize = float(self.EncoderConfig.get(self.paternName, 'encodeStripSize')) # Em metros
        
        for encoder in range(len(self.encoderXYpos)):
            print('A posição do encoder ' + str(encoder) + " é: " + str(self.encoderXYpos[encoder]))
        
        self.EncoderColors = []
        self.velocity      = 0.0
        self.QtdFrames     = 0

        self.newColor   = False

        print("GetVelocity initialized")

        # Essa variável é global pois não pode ser resetada toda vez queo o método
        # measure rodar novamente, o valor passado a ela aqui é figurativo.
        self.lastColor = [LabColor(lab_l=0.9, lab_a=16.3, lab_b=-2.22),
                          LabColor(lab_l=0.9, lab_a=16.3, lab_b=-2.22),
                          LabColor(lab_l=0.9, lab_a=16.3, lab_b=-2.22)]
        
        # Guarda o último tempo que houve uma alteração de faixa do encoder
        self.lastAtt = 0

    def measure(self):
        
        differences = [False, False]

        # Converte as cores do encoder para LAB
        LABEncoderColors = []
        for color in self.EncoderColors:
            color_RGB = sRGBColor(color[0], color[1], color[2])
            LABEncoderColors.append(convert_color(color_RGB, LabColor))
        
        try:
            # Itere entre as cores e identifica se houve mudança em algum encoder,
            # caso tenha alguma mudança, a lista "differences" irá receber TRUE
            # para o respectivo encoder

            for i in range(len(LABEncoderColors)):
                difference = delta_e_cie2000(LABEncoderColors[i], self.lastColor[i])

                if difference > 40:

                    differences[i] = True
                    self.lastColor[i] = LABEncoderColors[i]

            # Se todos os encoders tiverem sofrido alterações...
            if not False in differences:
                
                # Esse modo calcula a velocidade com base no tempo decorrido do processamento,
                # portanto caso o processamento de todo o código estiver sendo mais lento ou mais rápido
                # do que deveria ser, poderá ser observado com esse cálculo. O cenário ideal é que esse
                # valor seja igual ao modo "by_frame"
                if self.mode == 'by_real_time':
                    timeInterval  = timeit.default_timer() - self.lastAtt
                    timeInterval  = timeInterval / 60

                    self.velocity = self.encodeStripSize / timeInterval
                    self.lastAtt = timeit.default_timer()

                # Esse modo calcula a velocidade com base no frame rate real do render ou câmera, comparando
                # com o frame rate teórico
                elif self.mode == 'by_frame':
                    
                    self.velocity  = self.encodeStripSize / ((self.QtdFrames / self.framerate) / 60)
                    self.QtdFrames = 0

                self.lastAtt = timeit.default_timer()
            
        except:
            pass

        self.newColor = False

    def get(self, unit='m/min'):
        '''Retorna a velocidade com que a esteira está se movendo
        
        Você pode informar a unidade de medida que deseja por meio do parâmetro "unit=",\
        caso não seja informado, será utilizado por padrão a unidade "m/min"

        Você pode utilizar as seguintes unidades:
        - "m/min": Metros por Minuto
        - "m/sec": Metros por Segundo
        - "mm/sec": Milimetros por Segundo
        
        '''

        if unit == 'm/min':
            return self.velocity
        if unit == 'm/sec':
            return self.velocity / 60
        if unit == 'mm/sec':
            return self.velocity * (100 / 6)

    def sendEncoderColors(self, EncoderColors):
        self.EncoderColors = EncoderColors
        self.QtdFrames += 1

        self.measure()