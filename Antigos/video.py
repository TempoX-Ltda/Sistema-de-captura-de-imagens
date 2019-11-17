import cv2
import imutils
import timeit
import numpy as np

cap = cv2.VideoCapture('E:\Drive\TEMPOX\Dev\Visão Computacional\Python 1\opencv-tutorial\VID_20190531_071106.mp4')
#cap = cv2.VideoCapture(0)

fps = 30

largEquip = 1300                

vel_esteira = (18/60)*1000
razao_horizontal = vel_esteira / fps    # "resolução" horizontal de captura

mmperPixel = 1.94

print(str(mmperPixel) + ' mm/px')

m2 = 0
while True:
    ret, frame = cap.read()
    
    tempoinicio = timeit.default_timer()
    
    if ret == True:

        recorte = frame[50:910, 1:540]

        #cv2.imshow("Linha UV RGB", recorte)

        gray = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)         
        
        thresh = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY_INV)[1]
        
        resized2 = cv2.resize(thresh, (540, 910))
        '''
        inverter = cv2.bitwise_not(resized2)

        contours, hierarchy = cv2.findContours(inverter, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        cv2.drawContours(gray, contours, -1, (0,255,0), 1)

        #cv2.imshow("Linha UV RGB", gray)
        '''
        
        escanear = resized2.copy()

        scan = escanear[100:650 , 219:220]
        
        linergb = cv2.line(recorte,  (219,100), (219,650), (0,255,0),2)
        linebw  = cv2.line(resized2, (219,100), (219,650), (0,255,0),2)        
        
        pixels = 0

        for i in range(len(scan)):
            if scan[i] == 0:
                pixels += 1

        m2 += ((pixels * mmperPixel)*razao_horizontal)/1000000
        
        #text1 = "Existem {} pixels pretos!".format(pixels)
        font = cv2.FONT_HERSHEY_SIMPLEX        
        #cv2.putText(recorte,text1,(10,25), font, 1,(0,0,255),2,cv2.LINE_AA)
        text2 = "{:01.2f} Metros quadrados!".format(m2)        
        cv2.putText(recorte,text2,(10,60), font, 1,(0,0,255),2,cv2.LINE_AA)
        tempo = "{:0.1f} segundos".format(timeit.default_timer())         
        cv2.putText(recorte,tempo,(10,95), font, 1,(0,0,255),2,cv2.LINE_AA)

        cv2.imshow("Linha UV RGB", recorte)
        cv2.imshow("Linha UV BW", resized2)
        
        key = cv2.waitKey(1)
        
        if key == 27:
            break

    else:
        break

print("{:0.2f} M² processados".format(m2/13.5))
cap.release()
cv2.destroyAllWindows()
