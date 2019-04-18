#!/usr/bin/env python3

import urllib.request

class Config():

    def __init__(self):

        self.m_port = "8080"

        self.m_public_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        print('My public IP is :' + self.m_public_ip)

        self.m_android_address = 'localhost:8081'
        self.m_ai_address = 'localhost:8082'