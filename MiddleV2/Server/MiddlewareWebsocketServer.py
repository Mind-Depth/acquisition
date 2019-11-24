#!/usr/local/bin/python3

from Utils.PrintUtils import log
import threading
import socket
import json
import time

class MiddlewareWebsocketServer():
    def __init__(self, ip, port, fe_callback):
        self.m_ip = ip
        self.m_port = port
        self.m_fe_callback = fe_callback
        self.m_buff_read_size = 1024
        self.m_client_socket = None
        self.m_is_running = False
        self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.m_thread = threading.Thread(target = self.read_websocket)

    def connect_to_ore(self):
        log(self, 'Trying to connect ore websocket on {}:{}'.format(str(self.m_ip), self.m_port))
        self.m_socket.connect((self.m_ip, self.m_port))
        log(self, 'Successfuly connected to ore websocket {}:{}'.format(str(self.m_ip), self.m_port))

    def read_websocket(self):
        self.m_is_running = True
        while self.m_is_running:
            data = self.m_socket.recv(self.m_buff_read_size)
            log(self, 'Receiving data from websocket : {}'.format(data))
            self.m_fe_callback(json.dumps(data.decode('utf-8')))

    def start_mws(self):
        self.m_thread.start()
        
    def stop_server(self):
        log(self, 'Stopping the Middleware Websocket Server')
        if self.m_client_socket is None:
            log(self, 'Unable to close client connexion : null client socket')
        else:
            self.m_client_socket.close()
        if self.m_is_running:
            self.m_is_running = False
            self.m_thread.join()
