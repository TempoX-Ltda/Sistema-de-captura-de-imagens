import numpy as np
import cv2
import matplotlib.pyplot as plt
import threading

from classes.TX_ContornarPeca import ContornarPeca as CntPc

class Focar():

    def __init__(self):

        self.StackedParts = []
        self.threadLock = threading.Lock()

    def histogramMatPlotLib(self, image):
        fig, ax = plt.subplots()
        
        for i, col in enumerate(['b', 'g', 'r']):
            hist = cv2.calcHist([image], [i], None , [255], [0, 256])
            ax.plot(hist, color = col)
            fig.canvas.draw()
        
        X = np.array(fig.canvas.renderer.buffer_rgba())
        X = cv2.cvtColor(X, cv2.COLOR_BGRA2BGR)
        
        pc_height, pc_width, lx = image.shape 
        plt_height, plt_width, lx = X.shape
        num = pc_height / plt_height  
        
        X = cv2.resize(X, (int(plt_width*num), pc_height))
        
        image = np.concatenate((image, X), axis=1)
        
        return image
       
    def cutRectangle(self, contour, image, id_obj, precision, mask, hist=''):

        maskedimage = cv2.bitwise_and(image, image, mask = mask)
        

        # Desenha e separa cada peça por janela e calcula o tamanho da peça
        rect = cv2.minAreaRect(contour)
        box  = cv2.boxPoints(rect)
        box  = np.int0(box)
        (image_cut, widthA, heightA) = CntPc.four_point_transform(0, maskedimage, box)
        comp_pc = widthA  * precision
        larg_pc = heightA * precision


        with self.threadLock:
            self.StackedParts.append(image_cut)
        

        if hist == 'MatPlotLib':
            image_cut = Focar.histogramMatPlotLib(self, image_cut)
                    
        cv2.imshow('pc' + str(id_obj[1]), image_cut)

        return comp_pc, larg_pc