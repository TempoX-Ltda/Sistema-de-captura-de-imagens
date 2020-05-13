# -*- coding: utf-8 -*-

import sys
import requests
import json

def make_github_issue(repo_owner, repo_name, title, body=None, labels=None):

    # Authentication for user filing issue (must have read/write access to
    # repository to add issue to)
    TOKEN = 'd8a0370aeb991702d77ad012cd8bd07509b50af2'
    
    # Create an issue on github.com using the given parameters
    # Url to create issues via POST
    url = 'https://api.github.com/repos/%s/%s/import/issues' % (repo_owner, repo_name)
    
    # Headers
    headers = {
        "Authorization": "token %s" % TOKEN,
        "Accept": "application/vnd.github.golden-comet-preview+json"
    }
    
    # Create our issue
    data = {'issue': {'title': title,
                      'body': body,
                      'labels': labels}}

    payload = json.dumps(data)

    # Add the issue to our repository
    response = requests.request("POST", url, data=payload, headers=headers)
    if response.status_code == 202:
        print('Successfully created Issue "%s"' % title)
    else:
        print('Could not create Issue "%s"' % title)
        print('Response:', response.content)

'''
title = 'Pretty title'
body = 'Beautiful body'
labels = [
    "Testes"
]

make_github_issue(title, body, labels)
'''