import cv2
import imutils
import timeit
import numpy as np
import time
def escrever(imagem, texto, x, y):
    return(cv2.putText(imagem, texto, (x, y), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2,cv2.LINE_AA))

cap = cv2.VideoCapture('E:\Drive\TEMPOX\Dev\Visão Computacional\Python 1\opencv-tutorial\Peças brancas 2 por vez.mp4')
#cap = cv2.VideoCapture(0)

fps = 30

vel_esteira = (18/60)*1000
razao_horizontal = vel_esteira / fps    # "resolução" horizontal de captura

mmperPixel = 1.94

#print(str(mmperPixel) + ' mm/px')

m2 = 0
counterframe = 0

ret = True
objs_frame = []
objs_old = []
obj_atual  = []
objetos = []

idpeca = 1
obj_novo = False

last_obj = []
referencia = 100000
counterobj = 0

while True:
    ret, frame = cap.read()
    if ret != True:
        break

    counterframe += 1

    tempo_inicio = timeit.default_timer()

    resized = cv2.resize(frame, (960, 540))

    recort = resized[1:540, 120:800]

    rotated = imutils.rotate_bound(recort, 90)

    rotatedr = rotated[100:580, 1:540]

    gray = cv2.cvtColor(rotatedr, cv2.COLOR_BGR2GRAY)

    suave = cv2.blur(gray, (3,3))

    eroded = cv2.erode(suave, None, iterations=5)
    dilated = cv2.dilate(eroded, None, iterations=5)
    thresh = cv2.threshold(dilated, 190, 255, cv2.THRESH_BINARY)[1]
    (contours, lx) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    objs_old = objs_frame
    objs_frame = []
    obj_atual  = []
    

    for cnts in contours:

        quadroanterior = []
        M = cv2.moments(cnts)

        if M['m00'] != 0 and cv2.contourArea(cnts) > 20000:

            cX = int(M['m10'] / M['m00'])

            cY = int(M['m01'] / M['m00'])

            counterobj += 1
            
            print(counterobj)
            obj_atual = [counterframe,idpeca,cX,cY,cv2.contourArea(cnts)]

            if counterobj > 1:
                
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

            #Identifica o último objeto que passou           
            for i in range(len(objs_frame)):

                if objs_frame[i][2] < referencia:
                    referencia = objs_frame[i][2]
                    last_obj = objs_frame[i]
                
            escrever(rotatedr, 'Pc {}'.format(obj_atual[1]) , cX, cY)
            #escrever(grayr, '{} X'.format(cX)            , cX, cY-15)
            #escrever(grayr, '{} Y'.format(cY)            , cX, cY+15)       
            #escrever(grayr, '{:0.05f} M2'.format(obj_atual[4]/1000000*mmperPixel)  , cX, cY+45)       

    escanear = thresh.copy()
    scan = escanear[20:460 , 219:220]

    if counterframe == 1:
        imglog = scan
    else:
        for i in range(int(razao_horizontal/mmperPixel)): #isso pode dar problema pois está arredondando os valores
            imglog = np.concatenate((imglog, scan), axis=1)
    
    linegray = cv2.line(thresh, (219,20), (219, 460), (150), 2)
    linergb  = cv2.line(rotatedr , (219,20), (219, 460), (0  ,0,255), 2)

    pixels = cv2.countNonZero(scan)

    m2 += ((pixels * mmperPixel)*razao_horizontal)/1000000

    escrever(rotatedr, "{:01.2f} Metros quadrados!".format(m2)           , 10, 60)
    escrever(suave, "{:0.1f} segundos".format(timeit.default_timer()) , 10, 95)

    cv2.imshow("Linha UV BW", thresh)
    cv2.imshow("Linha UV rgb", rotatedr)

    if imglog.shape[1] < 1300:
        cv2.imshow("concat", imglog)
    else:
        cv2.imshow("concat", imglog[1:410, -1300:-1])
        
    #time.sleep(.1)

    key = cv2.waitKey(1) 
    if key == 27:
        break
            
print("{:0.2f} M² processados".format(m2))
cap.release()
cv2.destroyAllWindows()
