import cv2
from configparser import ConfigParser

class CalibrateRes():
    def __init__(self, video, alignClass, cameraAlignPath):
        self.video           = video
        self.Align           = alignClass
        self.clickPos        = []
        self.color           = []
        self.frame           = []
        self.cameraAlignPath = cameraAlignPath

        self.alignConfigs    = ConfigParser()
        self.alignConfigs.read(self.cameraAlignPath)

    def get_tresh_color(self):
        ret, frame = self.video.read()
        self.frame = self.Align.AlignFrame(frame, calibrateMode=True)

        windowName = 'Selecione um dos pontos de referencia' 
        cv2.namedWindow(windowName)
        
        # Passa para o cv2 que os eventos de mouse que forem efetuados na janela "windowName"
        # deverão executar o método "self.pickColorByClickPos"
        cv2.setMouseCallback(windowName, self.pickColorByClickPos)

        # Mostra a janela para clicar
        while ret:
            cv2.imshow(windowName, self.frame)

            key = cv2.waitKey(1) 
            if self.clickPos != []:
                break
            
        cv2.destroyAllWindows()

        # Coleta a cor do pixel onde foi feito o clique
        self.color = self.frame[self.clickPos[1], self.clickPos[0]]

    def pickColorByClickPos(self, event, x, y, flags, param):

        # Guarda a posição do mouse ao efetuar o clique
        if event == cv2.EVENT_LBUTTONDOWN:
            self.clickPos = [x, y]

        # Passa adiante caso outro evento do Mouse for executado
        else:
            pass
        
    def get_tresh(self):
        # Retorna somente os pixels da imagem que tiverem a cor semelhante a cor que foi selecionada
        # pelo usuário, esse precisão pode ser alterado conforme necessidade
        return cv2.inRange(self.frame, self.color - 10, self.color + 10)

    def calibrate(self, Section):

        self.get_tresh_color()
        img = self.get_tresh()
        
        # Encontra todos os contornos da imagem que comentém somente as marcações
        (contours, lx) = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        marks = {0:{'x': 0, 'y':0},
                1:{'x': 0, 'y':0},
                2:{'x': 0, 'y':0},
                3:{'x': 0, 'y':0}}
        
        # Itera entre os contornos (cada marcação) e guarda suas posições
        for num, contour in enumerate(contours):
            M = cv2.moments(contour)

            cX = int(M['m10'] / M['m00'])
            cY = int(M['m01'] / M['m00'])
            
            marks[num]['x'] = cX
            marks[num]['y'] = cY
            # Retorna um erro caso tenha exista mais que 4 marcações
            # Pode previnir que o usuário clique em algum ponto errado

            if num > 4:
                ValueError
        

        # Nos testes foi identificado que a marcação 0 e a marcação 3 eram opostas, e por isso poderiam ser utilizadas
        # como referência para realizar os cálculos
        Xdist = marks[0]['x'] - marks[3]['x']
        Ydist = marks[0]['y'] - marks[3]['y']
        
        # É retornado essa mensagem para que o usuário faça a alteração manual dos valores no arquivo
        # pois a biblioteca configparser não oferece suporte para realizar o update desa informação
        # diretamente no arquivo sem que sejam perdidos os comentários que estão dentro do arquivo
        print('Coloque os seguintes valores na seção "' + Section + '" do arquivo "' + str(self.cameraAlignPath) + '"')
        print('marksDistXpx=' + str(Xdist))
        print('marksDistYpx=' + str(Ydist))