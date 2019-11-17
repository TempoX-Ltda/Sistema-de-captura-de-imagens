import cv2
import imutils
import timeit
import numpy as np
import time

def escrever(imagem, texto, x, y):
    return(cv2.putText(imagem, texto, (x, y), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2,cv2.LINE_AA))

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


ret = True
objs_frame = []
objs_old = []
obj_atual  = []
objetos = []

idpeca = 1
obj_novo = False

last_obj = []
referencia = 100000
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
    
    objs_old = objs_frame
    objs_frame = []
    obj_atual  = []

    if counterframe == 226:
        print("")
    for cnts in contours:

        quadroanterior = []
        M = cv2.moments(cnts)

        if M['m00'] != 0 and cv2.contourArea(cnts) > 20000:

            cX = int(M['m10'] / M['m00'])

            cY = int(M['m01'] / M['m00'])
            
            #Identifica objeto novo

            counterobj +=1

            
            obj_atual = [counterframe,idpeca,cX,cY]

            #print("Obj atual: ")
            #print(obj_atual)

            if counterframe > 1:
                
                #print("Old:")
                #print(objs_old)


                
                if len(objs_old) != 0:
                    for i in range(len(objs_old)):

                        cXa = int(objs_old[i][2])

                        cYa = int(objs_old[i][3])

                        if abs(cXa - cX) < 50 and abs(cYa - cY) < 50:
                            obj_atual[1] = objs_old[i][1]
                            #print("Result:")
                            #print(obj_atual)
                            
                            #print("")
                            obj_novo = False
                            break
                        else:
                            obj_novo = True
                else:
                    if abs(cX - last_obj[2]) > 100:
                        obj_novo = True
                
                if obj_novo == True:
                    idpeca += 1    
                    obj_atual[1] = idpeca

            objetos.append(obj_atual)
            objs_frame.append(obj_atual)

            #Identifica objeto mais a direita do frame
            
            for i in range(len(objs_frame)):

                if objs_frame[i][2] < referencia:
                    referencia = objs_frame[i][2]
                    last_obj = objs_frame[i]
                
            escrever(grayr, 'Pc {}'.format(obj_atual[1]) , cX, cY-45)
            escrever(grayr, '{} X'.format(cX)          , cX, cY-15)
            escrever(grayr, '{} Y'.format(cY)          , cX, cY+15)              
    

    
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
    
    time.sleep(.01)

    if key == 27:
        break
            
#for i in range(len(BD)):
#    print(BD[i])
print("{:0.2f} M² processados".format(m2))
cap.release()
cv2.destroyAllWindows()
