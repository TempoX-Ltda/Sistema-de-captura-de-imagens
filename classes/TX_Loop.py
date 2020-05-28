#Autor: Gabriel Niziolek - 2019
#Tempox Automacoes Indutriais LTDA.
#GTRLP - Data de Testes

from pathlib import Path
import timeit
from time import sleep
import os
import cv2
import imutils
import numpy as np
from configparser import ConfigParser

from classes.TX_Foco import Focar
from classes.TX_QualityTest import QualityTest
from classes.TX_GetVelocity import getVelocity

class loop():

    def escrever(self, imagem, texto, x, y):
        return(cv2.putText(imagem, texto, (x, y), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2,cv2.LINE_AA))

    def loop(self, AlignClass, VideoTreshClass, opencvVideo):
        
        Align = AlignClass
        VT    = VideoTreshClass
        cap   = opencvVideo

        GeneralConfig = ConfigParser()
        GeneralConfig.read(r'classes\GeneralConfig.ini')

        Show_Main_Window    = GeneralConfig.getboolean('Window', 'Show_Main_Window')
        Show_Tresh_Window   = GeneralConfig.getboolean('Window', 'Show_Tresh_Window')
        Show_Log_Window     = GeneralConfig.getboolean('Window', 'Show_Log_Window')
        Show_separate_Parts = GeneralConfig.getboolean('Window', 'Show_separate_Parts')
        Draw_contours       = GeneralConfig.get('Window', 'Draw_contours')

        Get_Velocity               = GeneralConfig.getboolean('Modules', 'Get_Velocity')
        Use_QualityTest            = GeneralConfig.getboolean('Modules', 'QualityTest')
        
        if Show_separate_Parts == True:
            Histogram_plot = GeneralConfig.getboolean('Modules', 'Histogram_plot')
        else:
            Histogram_plot = False

        mmperPixel       = Align.mmByPx

        fps              = 30
        referencia       = 100000
        idpeca           = 1
        m2               = 0
        counterframe     = 0
        counterobj       = 0
        objs_frame       = []
        objs_old         = []
        obj_atual        = []
        objetos          = []
        pcs_inframe      = []
        last_obj         = []
        obj_novo         = False

        Foco = Focar()

        if Use_QualityTest == True:
            QT = QualityTest(VT.perfectPaternPath, Foco.StackedParts).start()

        if Get_Velocity == True:
            # Instância a classe para acompanhar a velocidade da esteira
            Velocity = getVelocity(Align.CameraConfigPath,
                                Align.paternName,
                                GeneralConfig.get('Modules', 'Get_Velocity_Mode'),
                                fps)

            encoderXYpos = Velocity.encoderXYpos
        else:
            print('O módulo de velocidade está desativado, será considerada para os cálculos uma velocidade de 18 metros/min')
            razao_horizontal = 0.0003 / fps # "resolução" horizontal de captura

        while True:
            ret, frame = cap.read()

            if ret != True: #Valida se o frame existe
                break
            
            if Get_Velocity == True: 
                razao_horizontal = (Velocity.get(unit='mm/sec')) / fps # "resolução" horizontal de captura
            
            counterframe   += 1
            objs_old        = objs_frame
            pcs_inframe_old = pcs_inframe
            objs_frame      = []
            obj_atual       = []
            pcs_inframe     = []

            #Inicia cronômetro
            tempo_inicio = timeit.default_timer()

            frame = Align.AlignFrame(frame)
            frame_to_parts = frame.copy()

            (contours, thresh) = VT.getPartsContours(frame)

            if Draw_contours.lower() == 'all':
                cv2.drawContours(frame, contours, -1, (0,255,0), 4)

            if Get_Velocity == True:
                EncoderColors    = []
                
                for pos in encoderXYpos:
                    EncoderColors.append(frame[pos[1], pos[0]])
                    #print(EncoderColors)
                Velocity.sendEncoderColors(EncoderColors)

                if Velocity.showEncoderPos == True:
                    for encoder in encoderXYpos:
                        frame = cv2.circle(frame, tuple(encoder), 15, (255, 0, 0), thickness=3, lineType=8, shift=0) 

            #try:
            for cnts in contours: # Itera entre os contornos do Frame
                
                if Draw_contours.lower() == 'by_parts':
                    cv2.drawContours(frame, [cnts], -1, (0,255,0), 4)

                quadroanterior = []
                
                M = cv2.moments(cnts)

                if M['m00'] != 0 and cv2.contourArea(cnts) > 20000: # Valor de área minimo para reconhecer como objeto
                    
                    cX = int(M['m10'] / M['m00'])
                    cY = int(M['m01'] / M['m00'])

                    counterobj += 1
                    obj_atual = [counterframe,idpeca,cX,cY,cv2.contourArea(cnts)]

                    if counterobj > 1:
                        if len(objs_old) != 0:
                            for i in range(len(objs_old)): # Itera para comparar obj atual com objs do frame anterior

                                cXa = int(objs_old[i][2])
                                cYa = int(objs_old[i][3])

                                # Verifica se a peça do frame anterior é a mesma do frame atual
                                # Utilizando como referência a posição na tela
                                if abs(cXa - cX) < 50 and abs(cYa - cY) < 50: 
                                    obj_atual[1] = objs_old[i][1]
                                    obj_novo = False
                                    break
                                else:
                                    obj_novo = True
                        else:
                            if abs(cX - last_obj[2]) > 100:
                                obj_novo = True
                        
                        if obj_novo == True: # ID +1
                            idpeca += 1    
                            obj_atual[1] = idpeca

                    objetos.append(obj_atual)
                    objs_frame.append(obj_atual)
                    pcs_inframe.append(obj_atual[1])
                    print(pcs_inframe)
                    # Identifica o último objeto que passou           
                    for i in range(len(objs_frame)):
                        if objs_frame[i][2] < referencia:
                            referencia = objs_frame[i][2]
                            last_obj = objs_frame[i]

                    # Mostra cada peça individualmente na tela, hist mostra também o histograma de cores                            
                    comp_pc, larg_pc = Foco.cutRectangle(cnts, frame_to_parts, obj_atual, mmperPixel, thresh, Show_separate_Parts, hist=Histogram_plot)

                    # Escreve na imagem
                    self.escrever(frame, 'Pc {}'.format(obj_atual[1])              , cX, cY)
                    self.escrever(frame, 'Comp {:0.1f}'.format(comp_pc)            , cX, cY-30)
                    self.escrever(frame, 'Larg {:0.1f}'.format(larg_pc)            , cX, cY+30)       
                    self.escrever(frame, '{:0.05f} M2'.format(obj_atual[4]/1000000*mmperPixel)  , cX, cY+60)
            #except:
            #    pass

            if Show_separate_Parts == True:
                # Destroi as janelas das peças que sairam do quadro
                for num_obj in pcs_inframe_old:
                    if not num_obj in pcs_inframe:
                        cv2.destroyWindow('pc' + str(num_obj))

            # Conta M2
            scan = thresh[Align.start_scan : Align.end_scan,
                            Align.scanlineYpos : Align.scanlineYpos+1]

            pixels = cv2.countNonZero(scan)
            m2 += ((pixels * mmperPixel)*razao_horizontal)/1000000

            if Show_Log_Window == True:                
                # Cria e monta a janela de "log"
                if counterframe == 1:
                    imglog = scan
                else:
                    for i in range(int(razao_horizontal/mmperPixel)): # isso pode dar problema pois está arredondando os valores
                        imglog = np.concatenate((imglog, scan), axis=1)
            
                if imglog.shape[1] < 1300:
                    cv2.imshow("Log", imglog)
                else:
                    cv2.imshow("Log", imglog[:, -1300:-1])
            
            # Desenha linhas e escreve na janela
            linegray = cv2.line(thresh,    (Align.scanlineYpos, Align.start_scan), (Align.scanlineYpos, Align.end_scan), (150),       2)
            linergb  = cv2.line(frame , (Align.scanlineYpos, Align.start_scan), (Align.scanlineYpos, Align.end_scan), (0, 0, 255), 2)
            self.escrever(frame, "{:01.2f} Metros quadrados!".format(m2)           , 10, 60)
            self.escrever(frame, "{:0.1f} segundos".format(timeit.default_timer()) , 10, 95)
            
            if Get_Velocity == True:
                self.escrever(frame, "{:01.2f} M/s".format(Velocity.get()), 10, 130)

            # Mostra os videos
            if Show_Tresh_Window == True:
                cv2.imshow("Linha UV BW", thresh)
            if Show_Main_Window == True:
                cv2.imshow("Linha UV rgb", frame)

            # Delay a partir de determinado frame
            #if counterframe > 60:    
            #   sleep(.1)

            # Tecla de escape do processo -> ESC
            key = cv2.waitKey(1) 
            if key == 27:
                break
            
        
        print(Foco.Parts)

        print("{:0.2f} M² processados".format(m2))
        cap.release()

        cv2.destroyAllWindows()

        if Use_QualityTest == True:    
            QT.stop()