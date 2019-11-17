import cv2

class VideoTresh:
    'Processa os Videos'
    def tresh_bt_cae(self, img): #Padrão BURITI CAEMMUN
        suave = cv2.blur(img, (5,5))
        hsv = cv2.cvtColor(suave,cv2.COLOR_BGR2HSV)
        eroded = cv2.erode(hsv, None, iterations=5)
        dilated = cv2.dilate(eroded, None, iterations=5)
        thresh_hsv = cv2.inRange(dilated, (10, 30, 132), (26, 77, 176)) #[ 10  30 132] [ 26 77 176]
        (contours, lx) = cv2.findContours(thresh_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return (contours, thresh_hsv)

    def tresh_bf_cae(self, img): #Padrão BRANCO FOSCO CAEMMUN
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        suave = cv2.blur(gray, (3,3))
        eroded = cv2.erode(suave, None, iterations=5)
        dilated = cv2.dilate(eroded, None, iterations=5)
        thresh = cv2.threshold(dilated, 190, 255, cv2.THRESH_BINARY)[1]
        (contours, lx) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return (contours, thresh)

    def tresh_esteira_branco(self, img): #Padrão Branco teste esteira
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        suave = cv2.blur(gray, (3,3))
        eroded = cv2.erode(suave, None, iterations=5)
        dilated = cv2.dilate(eroded, None, iterations=5)
        thresh = cv2.threshold(dilated, 190, 255, cv2.THRESH_BINARY)[1]
        (contours) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return (contours, thresh)