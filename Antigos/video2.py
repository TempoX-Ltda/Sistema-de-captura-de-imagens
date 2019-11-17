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

        resized = cv2.resize(frame, (960, 540))

        recort = resized[1:540, 120:800]

        rotated = imutils.rotate_bound(recort, 90)

        gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)

        thresh = cv2.threshold(gray.copy(), 190, 255, cv2.THRESH_BINARY)[1]

        canny1 = cv2.Canny(thresh, 10 , 20)

        escanear = thresh.copy()

        scan = escanear[100:600 , 219:220]

        linegray = cv2.line(thresh, (219,100), (219, 600), (255,255,255), 2)
        linergb = cv2.line(rotated, (219,100), (219, 600), (0,255,255), 2)

        pixels = 0

        for i in range(len(scan)):
            if scan[i] == 255:
                pixels += 1
        
        m2 += ((pixels * mmperPixel)*razao_horizontal)/1000000

                #text1 = "Existem {} pixels pretos!".format(pixels)
        font = cv2.FONT_HERSHEY_SIMPLEX        
        #cv2.putText(recorte,text1,(10,25), font, 1,(0,0,255),2,cv2.LINE_AA)
        text2 = "{:01.2f} Metros quadrados!".format(m2)        
        cv2.putText(rotated,text2,(10,60), font, 1,(0,0,255),2,cv2.LINE_AA)
        tempo = "{:0.1f} segundos".format(timeit.default_timer())         
        cv2.putText(rotated,tempo,(10,95), font, 1,(0,0,255),2,cv2.LINE_AA)

        cv2.imshow("Linha UV RGB", rotated)
        cv2.imshow("Linha UV BW", thresh)
        cv2.imshow("Linha UV canny", canny1)

        key = cv2.waitKey(1)
        
        if key == 27:
            break

    else:
        break

print("{:0.2f} M² processados".format(m2/13.5))
cap.release()
cv2.destroyAllWindows()
