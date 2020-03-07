# ===============================================================================
#    This sample illustrates how to grab and process images using the CInstantCamera class.
#    The images are grabbed and processed asynchronously, i.e.,
#    while the application is processing a buffer, the acquisition of the next buffer is done
#    in parallel.
#
#    The CInstantCamera class uses a pool of buffers to retrieve image data
#    from the camera device. Once a buffer is filled and ready,
#    the buffer can be retrieved from the camera object for processing. The buffer
#    and additional image data are collected in a grab result. The grab result is
#    held by a smart pointer after retrieval. The buffer is automatically reused
#    when explicitly released or when the smart pointer object is destroyed.
# ===============================================================================
from pypylon import pylon
from pypylon import genicam
import numpy as np
import cv2
import sys
import os
#os.environ["PYLON_CAMEMU"] = "1"

# The exit code of the sample application.
exitCode = 0
img_log = ''
try:
    # Create an instant camera object with the camera device found first.
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()

    # Print the model name of the camera.
    print("Using device ", camera.GetDeviceInfo().GetModelName())

    # Set parameters
    camera.Height.SetValue(1080)
    camera.Width.SetValue(4)
    #camera.AcquisitionFrameRateAbs.SetValue(60)

    # or Load parameters from a file
    #nodeFile = r'Basler_camera\Emulation_0815-0000.pfs'
    #print("Reading file back to camera's node map...")
    #pylon.FeaturePersistence.Load(nodeFile, camera.GetNodeMap(), True) # TODO verificar porque ocorre erro ao carregar o arquivo do pylon

    # The parameter MaxNumBuffer can be used to control the count of buffers
    # allocated for grabbing. The default value of this parameter is 10.
    camera.MaxNumBuffer = 5

    # Start the grabbing of c_countOfImagesToGrab images.
    # The camera device is parameterized with a default configuration which
    # sets up free-running continuous acquisition.
    camera.StartGrabbing()

    # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
    # when c_countOfImagesToGrab images have been retrieved.
    while camera.IsGrabbing():

        # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        # Image grabbed successfully?
        if grabResult.GrabSucceeded():

            # Access the image data.
            img = grabResult.Array
            
            if img_log == '':
                img_log = img
            else:
                img_log = np.concatenate((img_log, img), axis=1)
            print(img_log.shape)
            cv2.imshow('img', img_log)
            k = cv2.waitKey(1)
            if k == 27:
                break
        else:
            print("Error: ", grabResult.ErrorCode, grabResult.ErrorDescription)
        grabResult.Release()
    camera.Close()

except genicam.GenericException as e:

    # Error handling.
    print("An exception occurred.")
    print(e.GetDescription())
    exitCode = 1

sys.exit(exitCode)