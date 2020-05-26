
import os
import traceback

from configparser import ConfigParser
from pathlib import Path
import cv2

from classes.TX_Loop         import loop
from classes.TXVideoProcess  import VideoTresh, VideoAlign
from classes.TX_CalibrateRes import CalibrateRes
from classes.GitHub_Issue    import make_github_issue

def checkfile(arquivo):
    if not os.path.exists(arquivo):
        print('Caminho para arquivo de vídeo não existente! ' + str(arquivo))
        exit()
    else:
        print('Utilizando arquivo: ' + str(arquivo))
        pass

inputConfig = ConfigParser()
inputConfig.read(r"classes\InputConfig.ini")

method = 0

logpath = r'log/lastlog.txt'
log = open(logpath, 'w')

try:
    while True:

        # Mostra todas as possibilidades de métodos de video que o arquivo "InputConfig.ini" possui
        print('')
        for num, name in enumerate(inputConfig.sections()):
            num = num + 1
            print(str(num) + " - " + name)
        print('Digite "q" ou "Q" para sair.')

        # Coleta e valida a entrada do usuário
        close = False
        while True:
            try:
                response = input("Informe a forma de execução da análise:")
                
                if response.lower() == 'q':
                    close = True
                    break
                    
                else:
                    response = int(response)

                if response < len(inputConfig.sections()) + 1 and response != 0:
                    method = str(inputConfig.sections()[response - 1])
                    break
            except:
                pass

        if close == True:
            print("Finalizando código.")
            exit()

        videoPath = Path(inputConfig.get(method, "path"))

        cap = ''

        if inputConfig.get(method, "type") == "file":
            checkfile(videoPath)
            cap = cv2.VideoCapture(str(videoPath))
        elif inputConfig.get(method, "type") == "camera":
            cap = cv2.VideoCapture(int(videoPath))
        else:
            print('O tipo de execução não foi definido corretamente no arquivo "inputConfig.ini". Encerrando...')
            exit()

        cameraConfigPath = Path(r'classes\CameraConfig.ini')
        # Instância a classe para fazer o alinhamento/enquadramento dos frames
        # carregando as informações do arquivo que é passado
        Align = VideoAlign(cameraConfigPath)

        # Instância a classe para recortar os contornos das peças e realizar
        # o TRESH da imagem, carregando as informações do arquivo que é passado
        VT = VideoTresh(r'classes\ColorConfig.ini')

        # É passado o nome das configurações de enquadramento/alinhamento que estão no arquivo
        # "CameraConfig.ini" com base no método de vídeo do arquivo "InputConfig.ini"
        Align.selectPatern(inputConfig.get(method, "cameraAlign"))

        # É passado o nome das configurações de cor/padrão utilizado que estão no arquivo
        # "ColorConfig.ini" com base no método de vídeo do arquivo "InputConfig.ini"
        VT.selectPatern(inputConfig.get(method, "colorPatern"))

        while True:
            print('"c" para calibrar mm/px')
            print('"r" para rodar algoritmo')
            response = input()

            if response.lower() == 'r':
                L = loop()
                L.loop(Align, VT, cap)
                break

            elif response.lower() == 'c':
                Calibrate = CalibrateRes(cap, Align, cameraConfigPath)
                Calibrate.calibrate(inputConfig.get(method, "cameraAlign"))
                break

except Exception as Error:
    traceback.print_exc(file=log)
    log.close()   
    with open(logpath, 'r') as myfile:
        data = myfile.read()

    print(data)

    print('Ocorreu um erro que impede a continuação do sistema!\n')
    
    response = input("Deseja enviar esse log para análise? (S/N)")
    
    if response.lower() == "s" or response.lower() == "sim":
        make_github_issue('TempoX-Ltda', 'Gestao-Linha-UV', str(Error), body=str(data), labels=["Testes"])
    if response.lower() == "n" or response.lower() == "não":
        exit
