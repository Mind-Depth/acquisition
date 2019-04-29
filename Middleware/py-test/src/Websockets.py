#!/usr/bin/env python3

import socket
from Config import Config
from Middleware import Server

class Websockets:

    def __init__(self, callback):
        self.m_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.m_buff_read_size = 1024
        self.m_requestor_callback = callback

    def _connect(self, host, port):
        try:
            self.m_s.connect((host, port))
        except:
            print('Cannot establish the socket connection with ORengine')
            #TODO prevenir chicha et alex ou relancer
        
    def _read(self):
        while True:
            data = self.m_s.recv(self.m_buff_read_size)
            self.m_requestor_callback(data)