import cv2
import os
from templatematching import templateMatching
from matplotlib import pyplot as plt

tm = templateMatching(r'codigo do beneli\Analisequalidadeopencv\ImgPecas\padrao\padrao.jpg')



directory = r'codigo do beneli\Analisequalidadeopencv\ImgPecas'
for filename in os.listdir(directory):
    if filename.endswith(".jpg"):
        partPath = os.path.join(directory, filename)

        res, img = tm.find(partPath)

        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])

        plt.show()

    else:
        continue
