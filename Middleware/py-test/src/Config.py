#!/usr/bin/env python3

import urllib.request
import socket

class Config():

    def __init__(self, **kwargs):

        self.m_port = "8080"
        self.m_socket_port = "6669"
        self.m_socket_host = "localhost"
        self.m_debug = True
        self.m_android_route = '/biofeedback'
        self.m_ai_route = '/server'
        self.m_pipe_name = kwargs['pipe_name']
        self.m_server_to_client = kwargs['server_to_client']
        self.m_client_to_server = kwargs['client_to_server']

        self.m_public_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        self.m_local_ip = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
        print('My public IP is : ' + self.m_public_ip)
        print('My local IP is : ' + self.m_local_ip)

        self.m_android_address = 'http://192.168.1.13:8080'
        self.m_ai_address = 'http://localhost:4242'
