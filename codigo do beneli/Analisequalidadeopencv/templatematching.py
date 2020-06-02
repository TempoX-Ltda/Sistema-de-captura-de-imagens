import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt



class templateMatching():

    def __init__(self, paternPath):
        img = cv.imread(paternPath,0)
        self.img2 = img.copy()

    def find(self, partPath):
        template = cv.imread(partPath,0)
        w, h = template.shape[::-1]

        # All the 6 methods for comparison in a list
        methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
                    'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

        for meth in methods:
            img = self.img2.copy()
            method = eval(meth)

            # Apply template Matching
            res = cv.matchTemplate(img,template,method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)

            cv.rectangle(img,top_left, bottom_right, 255, 2)


        return (res, img)


            