from pypylon import pylon
import cv2
import os
import platform

#os.environ["PYLON_CAMEMU"] = "1"
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

imgPy = pylon.PylonImage()
camera.StartGrabbing()
frame = 0
while camera.IsGrabbing():
    frame +=1
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        imgPy.AttachGrabResultBuffer(grabResult)
        if platform.system() == 'Windows':
            # The JPEG format that is used here supports adjusting the image
            # quality (100 -> best quality, 0 -> poor quality).
            ipo = pylon.ImagePersistenceOptions()
            ipo.SetQuality(100)
            filename = "Basler_camera\imgs\saved_pypylon_img_%d.jpeg" % frame
            imgPy.Save(pylon.ImageFileFormat_Jpeg, filename, ipo)

        # Access the image data.
        #print("SizeX: ", grabResult.Width)
        #print("SizeY: ", grabResult.Height)
        img = grabResult.Array
        #print("Gray value of first pixel: ", img[0, 0])
        img = cv2.resize(img, (1780,1024))
        cv2.imshow('img', img)
        k = cv2.waitKey(1)
        if k == 27:
            break

    grabResult.Release()