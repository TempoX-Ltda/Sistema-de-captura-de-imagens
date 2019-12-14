#Autor: Gabriel Niziolek - 2019
#Tempox Automacoes Indutriais LTDA.
#GTRLP - Data de Testes

import timeit
from time import sleep

import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt

from classes.TXVideoProcess import VideoTresh as VT
from classes.TX_Foco import Focar

m2 = 0
cap = ''

def self():
    pass

def escrever(imagem, texto, x, y):
    return(cv2.putText(imagem, texto, (x, y), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2,cv2.LINE_AA))

def AbreVideo():  
    #Valida entradas dos padrões
    padroes_aceitos = [0, 1, 2, 9]
    while True:
        padrao = int(input('Informe o padrão: \n(0) - BRANCO 628x607 \n(1) - BRANCO 2pcs CM \n(2) - BURITI CM \n(9) - TESTE ESTEIRA BRANCO \n\n'))
        
        if padrao in padroes_aceitos:
            break
        else:
            print('Erro, Digite corretamente!!')

    #Carrega arquivo do vídeo
    global cap
    if padrao == 0:
        cap = cv2.VideoCapture('Videos Teste\Porta Branca 628x607.mp4')

    elif padrao == 1:
        cap = cv2.VideoCapture('Videos Teste\Peças brancas 2 por vez.mp4')

    elif padrao == 2:
        cap = cv2.VideoCapture('Videos Teste\Peça Marrom.mp4')

    elif padrao == 9:
        cap = cv2.VideoCapture(0)

    fps              = 30
    vel_esteira      = (18/60)*1000
    razao_horizontal = vel_esteira / fps # "resolução" horizontal de captura
    referencia       = 100000
    mmperPixel       = 1.94
    idpeca           = 1
    global m2
    
    counterframe     = 0
    counterobj       = 0
    objs_frame       = []
    objs_old         = []
    obj_atual        = []
    objetos          = []
    pcs_inframe      = []
    last_obj         = []
    obj_novo         = False

    while True:
        ret, frame = cap.read()
        if ret != True: #Valida se o frame existe
            break


        counterframe   += 1
        objs_old        = objs_frame
        pcs_inframe_old = pcs_inframe
        objs_frame      = []
        obj_atual       = []
        pcs_inframe     = []

        #Inicia cronômetro
        tempo_inicio = timeit.default_timer()

        #Escolhe qual processo de mascara será utilizado com base em cada padrão
        if padrao == 0:
            resized = cv2.resize(frame, (960, 540))
            recort = resized[1:540, 120:800]
            rotatedr = imutils.rotate_bound(recort, 90)
            (contours, thresh) = VT.tresh_bf_cae(0, rotatedr)
            start_scan = 20
            end_scan   = 600
            
        elif padrao == 1:
            resized = cv2.resize(frame, (960, 540))
            recort = resized[1:540, 150:750]
            rotatedr = imutils.rotate_bound(recort, 90)
            (contours, thresh) = VT.tresh_bf_cae(0, rotatedr)
            start_scan = 20
            end_scan   = 550
            
        elif padrao == 2:
            resized = cv2.resize(frame, (960, 540))
            recort = resized[1:540, 120:800]
            rotatedr = imutils.rotate_bound(recort, 90)
            (contours, thresh) = VT.tresh_bt_cae(0, rotatedr)
            start_scan = 20
            end_scan   = 450
            
        elif padrao == 9:
            rotatedr = frame
            (contours, thresh) = VT.tresh_esteira_branco(0, rotatedr)
            start_scan = 20
            end_scan   = 450
        try:
            for cnts in contours: #Itera entre os contornos do Frame

                quadroanterior = []
                
                M = cv2.moments(cnts)

                if M['m00'] != 0 and cv2.contourArea(cnts) > 20000: #Valor de área minimo para reconhecer como objeto
                    
                    cX = int(M['m10'] / M['m00'])
                    cY = int(M['m01'] / M['m00'])

                    counterobj += 1
                    obj_atual = [counterframe,idpeca,cX,cY,cv2.contourArea(cnts)]

                    if counterobj > 1:
                        if len(objs_old) != 0:
                            for i in range(len(objs_old)): #Itera para comparar obj atual com objs do frame anterior

                                cXa = int(objs_old[i][2])
                                cYa = int(objs_old[i][3])

                                if abs(cXa - cX) < 50 and abs(cYa - cY) < 50: #Verifica se a peça do frame anterior é a mesma do frame atual
                                    obj_atual[1] = objs_old[i][1]
                                    obj_novo = False
                                    break
                                else:
                                    obj_novo = True
                        else:
                            if abs(cX - last_obj[2]) > 100:
                                obj_novo = True
                        
                        if obj_novo == True: #ID +1
                            idpeca += 1    
                            obj_atual[1] = idpeca

                    objetos.append(obj_atual)
                    objs_frame.append(obj_atual)
                    pcs_inframe.append(obj_atual[1])

                    #Identifica o último objeto que passou           
                    for i in range(len(objs_frame)):
                        if objs_frame[i][2] < referencia:
                            referencia = objs_frame[i][2]
                            last_obj = objs_frame[i]

                    #Mostra cada peça indivdualmente na tela, hist ostra também o histograma de cores
                    comp_pc, larg_pc = Focar.cutRectangle(self, cnts, rotatedr, obj_atual, mmperPixel, hist = 'MatPlotLib')
                    
                    #Escreve na imagem
                    escrever(rotatedr, 'Pc {}'.format(obj_atual[1])              , cX, cY)
                    escrever(rotatedr, 'Comp {:0.1f}'.format(comp_pc)            , cX, cY-30)
                    escrever(rotatedr, 'Larg {:0.1f}'.format(larg_pc)            , cX, cY+30)       
                    #escrever(rotatedr, '{:0.05f} M2'.format(obj_atual[4]/1000000*mmperPixel)  , cX, cY+45)
        except:
            pass
        
        #Destroi as janelas das peças que sairam do quadro
        for num_obj in pcs_inframe_old:
            if not num_obj in pcs_inframe:
                cv2.destroyWindow('pc' + str(num_obj))

        escanear = thresh.copy()
        scan = escanear[start_scan:end_scan , 219:220]
        
        #Cria e monta a janela de "log"
        if counterframe == 1:
            imglog = scan
        else:
            for i in range(int(razao_horizontal/mmperPixel)): #isso pode dar problema pois está arredondando os valores
                imglog = np.concatenate((imglog, scan), axis=1)
        
        if imglog.shape[1] < 1300:
            cv2.imshow("Log", imglog)
        else:
            cv2.imshow("Log", imglog[1:410, -1300:-1])
        
        #Desenha linhas e escreve na janela
        linegray = cv2.line(thresh,    (219, start_scan), (219, end_scan), (150),       2)
        linergb  = cv2.line(rotatedr , (219, start_scan), (219, end_scan), (0, 0, 255), 2)
        escrever(rotatedr, "{:01.2f} Metros quadrados!".format(m2)           , 10, 60)
        escrever(rotatedr, "{:0.1f} segundos".format(timeit.default_timer()) , 10, 95)

        #Conta M2
        pixels = cv2.countNonZero(scan)
        m2 += ((pixels * mmperPixel)*razao_horizontal)/1000000

        #Mostra os videos
        cv2.imshow("Linha UV BW", thresh)
        cv2.imshow("Linha UV rgb", rotatedr)

        #Delay a partir de determinado frame
        #if counterframe > 60:    
        #   sleep(.1)

        if __name__ == "__main__":
            #Tecla de escape do processo -> ESC
            key = cv2.waitKey(1) 
            if key == 27:
                break
            cv2.imshow("Linha UV BW", thresh)
            cv2.imshow("Linha UV rgb", rotatedr)
        
    
    print("{:0.2f} M² processados".format(m2))
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    AbreVideo()
