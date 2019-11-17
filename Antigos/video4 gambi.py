import cv2
import imutils
import timeit
import numpy as np
import time

def escrever(imagem, texto, x, y):
    return(cv2.putText(imagem, texto, (x, y), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2,cv2.LINE_AA))

def busca(array, coluna, valor):
    retorno = []
    for i in range(len(array)):
        if array[i][coluna-1] == valor:
            #print(array[i])
            retorno.append(array[i])
    return(retorno)

cap = cv2.VideoCapture('E:\Drive\TEMPOX\Dev\Visão Computacional\Python 1\opencv-tutorial\VID_20190531_071106.mp4')
#cap = cv2.VideoCapture(0)

fps = 30

largEquip = 1300                

vel_esteira = (18/60)*1000
razao_horizontal = vel_esteira / fps    # "resolução" horizontal de captura

mmperPixel = 1.94

print(str(mmperPixel) + ' mm/px')

m2 = 0
counterframe = 0

BD = []
idPeca = 0
idDisp = 1
ret = True

positions = []
last_positions = []
while True:
    ret, frame = cap.read()
    if ret != True:
        break

    counterframe += 1

    tempoinicio = timeit.default_timer()
    
    resized = cv2.resize(frame, (960, 540))

    recort = resized[1:540, 120:800]

    rotated = imutils.rotate_bound(recort, 90)

    gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)

    #suave = cv2.blur(gray, (20,20))

    grayr = gray[100:580, 1:540]

    thresh = cv2.threshold(grayr, 190, 255, cv2.THRESH_BINARY)[1]

    (contours, lx) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #draw = cv2.drawContours(gray,contours,0 ,(0,255,255),3)

    
    counterobj = 0
    
    last_positions = positions
    positions = []
    for cnts in contours:

        quadroanterior = []
        M = cv2.moments(cnts)

        if M['m00'] != 0 and cv2.contourArea(cnts) > 1000:

            cX = int(M['m10'] / M['m00'])

            cY = int(M['m01'] / M['m00'])
            
            #escrever(grayr, 'Pc {}'.format(counterobj) , cX, cY-45)
            #escrever(grayr, '{} X'.format(cX)          , cX, cY-15)
            #escrever(grayr, '{} Y'.format(cY)          , cX, cY+15)              
            positions.append(cX)
    
    melhores_index = []
    menor_distancia = 50000
    for i in range(len(positions)):
        for j in range(len(last_positions)):
            if (last_positions[i] - positions[i] < menor_distancia):
                menor_distancia = last_positions[i] - positions[i]
        escrever(grayr, '{} X'.format(menor_distancia)          , positions[i], cY-15)



    

    escanear = thresh.copy()

    scan = escanear[40:450 , 219:220]

    linegray = cv2.line(thresh, (219,40), (219, 450), (255,255,255), 2)
    linergb  = cv2.line(grayr , (219,40), (219, 450), (0  ,255,255), 2)

    pixels = 0

    for i in range(len(scan)):
        if scan[i] == 255:
            pixels += 1
    
    m2 += ((pixels * mmperPixel)*razao_horizontal)/1000000

    escrever(grayr, "{:01.2f} Metros quadrados!".format(m2)           , 10, 60)
    escrever(grayr, "{:0.1f} segundos".format(timeit.default_timer()) , 10, 95)

    cv2.imshow("Linha UV BW", thresh)
    cv2.imshow("Linha UV rgb", grayr)

    key = cv2.waitKey(1) 
    
    time.sleep(0.1)

    if key == 27:
        break
            
#for i in range(len(BD)):
#    print(BD[i])
print("{:0.2f} M² processados".format(m2/13.5))
cap.release()
cv2.destroyAllWindows()
