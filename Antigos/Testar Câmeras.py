import cv2

def nothing(x):
    pass  

cap = cv2.VideoCapture(1)

cv2.namedWindow('Trackbars', 0)

cv2.createTrackbar('CAP_PROP_POS_MSEC', 'Trackbars', 1, 500, nothing)

cv2.createTrackbar('CAP_PROP_BRIGHTNESS', 'Trackbars', 1, 100, nothing)
cv2.createTrackbar('CAP_PROP_CONTRAST', 'Trackbars', 1, 100, nothing)
cv2.createTrackbar('CAP_PROP_SATURATION', 'Trackbars', 1, 100, nothing)
cv2.createTrackbar('CAP_PROP_HUE', 'Trackbars', 1, 100, nothing)
cv2.createTrackbar('CAP_PROP_GAIN', 'Trackbars', 1, 100, nothing)
cv2.createTrackbar('CAP_PROP_EXPOSURE', 'Trackbars', 1, 100, nothing)

while True:
    pos = cv2.getTrackbarPos('CAP_PROP_POS_MSEC', 'Trackbars')

    brightness = cv2.getTrackbarPos('CAP_PROP_BRIGHTNESS', 'Trackbars')
    contrast = cv2.getTrackbarPos('CAP_PROP_CONTRAST', 'Trackbars')
    sat = cv2.getTrackbarPos('CAP_PROP_SATURATION', 'Trackbars')
    hue = cv2.getTrackbarPos('CAP_PROP_HUE', 'Trackbars')
    gain = cv2.getTrackbarPos('CAP_PROP_GAIN', 'Trackbars')
    exp = cv2.getTrackbarPos('CAP_PROP_EXPOSURE', 'Trackbars')
    
    cap.set(0, pos)
    cap.set(10, brightness)
    cap.set(11, contrast)
    cap.set(12, sat)
    cap.set(13, hue)
    cap.set(14, gain)
    cap.set(15, exp*(-1))

    ret, frame = cap.read()
    
    cv2.imshow("camera 0", frame)
    
    key = cv2.waitKey(1) 
    if key == 27:
        break

cv2.destroyAllWindows()
