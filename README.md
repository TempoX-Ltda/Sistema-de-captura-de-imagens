# Gestao-Linha-UV

## Utilização básica

- Execute o código "main.py" que está na pasta raiz
- Escolha alguma das opções disponíveis para teste.
- Os arquivos do vídeo estão na pasta "Videos Teste"

## Inserção de novos renders de teste ou nova câmera

1. Adicione o arquivo de vídeo na pasta "Renders" e copie o caminho do arquivo;
2. Adicione uma nova seção no arquivo "InputConfig.ini" tendo como nome algo que identifique o render;
3. Configure os parâmetros de acordo:
    - *type*: identifica o tipo do input, no caso dos renders deve ser sempre igual a "file", no caso de câmeras deve ser igual a "camera";
    - *path*: caminho relativo para o arquivo do render, caso esteja configurando uma câmera plug'n play, deve ser o número de identificação da câmera no pc;
    - *cameraAlign*: nome da seção de configuração de enquadramento de imagem do arquivo "CameraConfig.ini", geralmente vai ser sempre igual para todos os renders ou câmera que são na mesma posição;
    - *colorPatern*: nome da seção de configuração de padrão de cor do arquivo "ColorConfig.ini", geralmente vai ser sempre igual para todos os renders que tem a mesa cor de peças;