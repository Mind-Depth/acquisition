#!/usr/bin/env python3

import socket
from Config import Config

class Websockets:

    def __init__(self):
        self.m_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.m_buff_read_size = 1024

    def _connect(self, host, port):
        try:
            self.m_s.connect((host, port))
        except:
            print('Cannot establish the socket connection with ORengine')
            return False
        
    def _read(self, requestor_callback):
        while True:
            data = self.m_s.recv(self.m_buff_read_size)
            requestor_callback(data)