from pypylon import pylon
import cv2
import os

#os.environ["PYLON_CAMEMU"] = "1"
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())


camera.StartGrabbing()

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data.
        #print("SizeX: ", grabResult.Width)
        #print("SizeY: ", grabResult.Height)
        img = grabResult.Array
        #print("Gray value of first pixel: ", img[0, 0])
        #img = cv2.resize(img, (1780,1024))
        cv2.imshow('img', img)
        k = cv2.waitKey(1)
        if k == 27:
            break

    grabResult.Release()