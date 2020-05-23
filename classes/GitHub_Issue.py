# -*- coding: utf-8 -*-

import sys
import requests
import json
from configparser import ConfigParser

def make_github_issue(repo_owner, repo_name, title, body=None, labels=None):

    # Authentication for user filing issue (must have read/write access to
    # repository to add issue to)
    #TOKEN = 'd8a0370aeb991702d77ad012cd8bd07509b50af2'
    
    configs = ConfigParser()
    configs.read('classes\GeneralConfig.ini')

    # Create an issue on github.com using the given parameters
    # Url to create issues via POST
    url = 'https://api.github.com/repos/%s/%s/import/issues' % (repo_owner, repo_name)
    
    # Headers
    headers = {
        "Authorization": "token %s" % configs.get('Bots', 'Issue_Bot_Token'),
        "Accept": "application/vnd.github.golden-comet-preview+json"
    }
    #print(headers)

    # Create our issue
    data = {'issue': {'title': title,
                      'body': body,
                      'labels': labels}}

    payload = json.dumps(data)

    #print(payload)

    # Add the issue to our repository
    response = requests.request("POST", url, data=payload, headers=headers)
    if response.status_code == 202:
        print('Foi enviado com sucesso o log de erros para a TempoX! \n O nome do seu chamado é: "%s"' % title)
    else:
        print('Não foi possível enviar o log para a TempoX, nome do erro: "%s"' % title)
        print('Resposta:', response.content)

if __name__ == '__main__':
    title = 'Pretty title'
    body = 'Beautiful body'
    labels = [
        "Testes"
    ]

    make_github_issue('TempoX-Ltda', 'Gestao-Linha-UV', title, body=body, labels=labels)
