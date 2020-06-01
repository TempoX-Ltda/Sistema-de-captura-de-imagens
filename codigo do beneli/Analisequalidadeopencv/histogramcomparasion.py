from __future__ import print_function
from __future__ import division
import cv2 as cv
import numpy as np
import argparse

#Lê as imagens no diretório
padrao = cv.imread('Analisequalidadeopencv\padrao.jpg')
peca = cv.imread('Analisequalidadeopencv\peca1.jpg')

#Divide as imagens nos três planos de cor
bgr_padrao = cv.split(padrao)
bgr_peca = cv.split(peca)

#Número de bins (subdivisão das dimensões de intensidade de cor)
histSize = 256
histRange = (0, 256) # the upper boundary is exclusive
accumulate = False

#Calculo do histograma em RGB do padrão ADICIONAR REGIÃO DA MASK ORIUNDO DO TEMPLATE MATCHING
b_histpadrao = cv.calcHist(bgr_padrao, [0], None, [histSize], histRange, accumulate=accumulate)
g_histpadrao = cv.calcHist(bgr_padrao, [1], None, [histSize], histRange, accumulate=accumulate)
r_histpadrao = cv.calcHist(bgr_padrao, [2], None, [histSize], histRange, accumulate=accumulate)

#Calculo do histograma em RGB da peça
b_histpeca = cv.calcHist(bgr_peca, [0], None, [histSize], histRange, accumulate=accumulate)
g_histpeca = cv.calcHist(bgr_peca, [1], None, [histSize], histRange, accumulate=accumulate)
r_histpeca = cv.calcHist(bgr_peca, [2], None, [histSize], histRange, accumulate=accumulate)






cv.waitKey()