from pypylon import pylon 
import cv2
import os
import numpy as np
os.environ["PYLON_CAMEMU"] = "1"

'''
# Pypylon get camera by serial number
serial_number = '22716154'
for i in pylon.TlFactory.GetInstance().EnumerateDevices():
    if i.GetSerialNumber() == serial_number:
        info = i
        break
else:
    print('Camera with {} serial number not found'.format(serial_number))
'''
# VERY IMPORTANT STEP! To use Basler PyPylon OpenCV viewer you have to call .Open() method on you camera

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()
from pypylon_opencv_viewer import BaslerOpenCVViewer



# Example of configuration for basic RGB camera's features
VIEWER_CONFIG_RGB_MATRIX = {
    "features": [
        {
            "name": "GainRaw",
            "type": "int",
            "step": 1,
        },
        {
            "name": "Height",
            "type": "int",
            "value": 1080,
            "unit": "px",
            "step": 2,
        },
        {
            "name": "Width",
            "type": "int",
            "value": 1920,
            "unit": "px",
            "step": 2,
        },
        {
            "name": "OffsetX",
            "type": "int",
            "dependency": {"CenterX": False},
            "unit": "px",
            "step": 2,
        },
        {
            "name": "OffsetY",
            "type": "int",
            "dependency": {"CenterY": False},
            "unit": "px",
            "step": 2,
        },
        {
            "name": "AcquisitionFrameRateAbs",
            "type": "int",
            "unit": "fps",
            "dependency": {"AcquisitionFrameRateEnable": True},
            "max": 150,
            "min": 1,
        },
        {
            "name": "AcquisitionFrameRateEnable",
            "type": "bool",
        },
        {
            "name": "ExposureTimeAbs",
            "type": "int",
            "dependency": {"ExposureAuto": "Off"},
            "unit": "μs",
            "step": 100,
            "max": 35000,
            "min": 500,
        },
    ],
    "features_layout": [
        ("Height", "Width"), 
        ("OffsetX", "CenterX"), 
        ("OffsetY", "CenterY"), 
        ("ExposureAuto", "ExposureTimeAbs"),
        ("AcquisitionFrameRateAbs", "AcquisitionFrameRateEnable"),
        ("BalanceWhiteAuto", "GainRaw")
    ],
    "actions_layout": [
        ("StatusLabel"),
        ("SaveConfig", "LoadConfig", "ContinuousShot", "SingleShot"), 
        ("UserSet")
    ],
    "default_user_set": "UserSet3",
                            }

#viewer.set_configuration(VIEWER_CONFIG_RGB_MATRIX)

#viewer.save_image('Basler_camera\img.png')

#img = viewer.get_image()

while True:
    viewer = BaslerOpenCVViewer(camera)
    img = viewer.get_image()
    cv2.imshow('img', img)

    k = cv2.waitKey(1)
    if k == 27:
        break