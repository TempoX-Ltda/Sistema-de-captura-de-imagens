from __future__ import print_function
from __future__ import division
import cv2 as cv
import numpy as np
import argparse




#############################################################  
################## CALCULO DO HISTOGRAMA ####################
############################################################# 

#Carrega a imagem do diretório 
parser = argparse.ArgumentParser(description='Code for Histogram Calculation tutorial.')
parser.add_argument('--input', default='Analisequalidadeopencv\padrao.jpg')#caminho para o ROI padrão
parser.add_argument('--input1', default='Analisequalidadeopencv\padrao.jpg')#caminho para a peça a ser analisada
args = parser.parse_args()
roipadrao = cv.imread(cv.samples.findFile(args.input))
pecanalisar = cv.imread(cv.samples.findFile(args.input1))



#Separa a imagem do padrão em três planos RGB, o output será um vetor de Mat  
bgr_planespadrao = cv.split(roipadrao)

#Separa a imagem da peça a ser analisada em três planos RGB, o output será um vetor de Mat  
bgr_planespeca = cv.split(pecanalisar)

#Número de bins (subdivisão das dimensões de intensidade de cor)
histSize = 256
histRange = (0, 256) # the upper boundary is exclusive
accumulate = False

#Calculo do histograma em RGB do padrão ADICIONAR REGIÃO DA MASK ORIUNDO DO TEMPLATE MATCHING
b_histpadrao = cv.calcHist(bgr_planespadrao, [0], None, [histSize], histRange, accumulate=accumulate)
g_histpadrao = cv.calcHist(bgr_planespadrao, [1], None, [histSize], histRange, accumulate=accumulate)
r_histpadrao = cv.calcHist(bgr_planespadrao, [2], None, [histSize], histRange, accumulate=accumulate)

#Calculo do histograma em RGB da peça
b_histpeca = cv.calcHist(bgr_planespeca, [0], None, [histSize], histRange, accumulate=accumulate)
g_histpeca = cv.calcHist(bgr_planespeca, [1], None, [histSize], histRange, accumulate=accumulate)
r_histpeca = cv.calcHist(bgr_planespeca, [2], None, [histSize], histRange, accumulate=accumulate)


#Cria uma imagem para exibir os histogramas RGB do padrão
hist_w = 512
hist_h = 400
bin_w = int(round( hist_w/histSize ))
histogramapadrao = np.zeros((hist_h, hist_w, 3), dtype=np.uint8)
cv.normalize(b_histpadrao, b_histpadrao, alpha=0, beta=hist_h, norm_type=cv.NORM_MINMAX)
cv.normalize(g_histpadrao, g_histpadrao, alpha=0, beta=hist_h, norm_type=cv.NORM_MINMAX)
cv.normalize(r_histpadrao, r_histpadrao, alpha=0, beta=hist_h, norm_type=cv.NORM_MINMAX)
for i in range(1, histSize):
    cv.line(histogramapadrao, ( bin_w*(i-1), hist_h - int(np.round(b_histpadrao[i-1])) ),
            ( bin_w*(i), hist_h - int(np.round(b_histpadrao[i])) ),
            ( 255, 0, 0), thickness=2)
    cv.line(histogramapadrao, ( bin_w*(i-1), hist_h - int(np.round(g_histpadrao[i-1])) ),
            ( bin_w*(i), hist_h - int(np.round(g_histpadrao[i])) ),
            ( 0, 255, 0), thickness=2)
    cv.line(histogramapadrao, ( bin_w*(i-1), hist_h - int(np.round(r_histpadrao[i-1])) ),
            ( bin_w*(i), hist_h - int(np.round(r_histpadrao[i])) ),
            ( 0, 0, 255), thickness=2)

#Cria uma imagem para exibir os histogramas RGB da peça
hist_w = 512
hist_h = 400
bin_w = int(round( hist_w/histSize ))
histogramapeca = np.zeros((hist_h, hist_w, 3), dtype=np.uint8)
cv.normalize(b_histpeca, b_histpeca, alpha=0, beta=hist_h, norm_type=cv.NORM_MINMAX)
cv.normalize(g_histpeca, g_histpeca, alpha=0, beta=hist_h, norm_type=cv.NORM_MINMAX)
cv.normalize(r_histpeca, r_histpeca, alpha=0, beta=hist_h, norm_type=cv.NORM_MINMAX)
for i in range(1, histSize):
    cv.line(histogramapeca, ( bin_w*(i-1), hist_h - int(np.round(b_histpeca[i-1])) ),
            ( bin_w*(i), hist_h - int(np.round(b_histpeca[i])) ),
            ( 255, 0, 0), thickness=2)
    cv.line(histogramapeca, ( bin_w*(i-1), hist_h - int(np.round(g_histpeca[i-1])) ),
            ( bin_w*(i), hist_h - int(np.round(g_histpeca[i])) ),
            ( 0, 255, 0), thickness=2)
    cv.line(histogramapeca, ( bin_w*(i-1), hist_h - int(np.round(r_histpeca[i-1])) ),
            ( bin_w*(i), hist_h - int(np.round(r_histpeca[i])) ),
            ( 0, 0, 255), thickness=2)

#Exibição das imagens e histogramas 
cv.imshow('Imagem da peca', pecanalisar)
cv.imshow('calcHist peca', histogramapeca)
cv.imshow('Imagem do padrao', roipadrao)
cv.imshow('calcHist padrao', histogramapadrao)



#############################################################  
################## HISTOGRAM COMPARASION ####################
############################################################# 
 

comparison = cv.compareHist(histogramapadrao, histogramapeca, cv.HISTCMP_CHISQR)


cv.waitKey()