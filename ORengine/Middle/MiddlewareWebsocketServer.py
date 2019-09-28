#!/usr/local/bin/python3

from PrintUtils import log
import threading
import socket
import json

class MiddlewareWebsocketServer():
    def __init__(self, ip, port):
        self.m_ip = ip
        self.m_port = port
        self.m_socket = socket.socket()
        self.m_thread = threading.Thread(target = self.run_serv)

    def run_serv(self):
        self.m_is_running = True
        self.m_socket.bind((self.m_ip, self.m_port))
        while True:
            self.m_socket.listen()
            self.m_client_socket, address = self.m_socket.accept()
            log(self, 'Connection from: {}'.format(str(address)))
            while True:
                try:
                    data = self.m_client_socket.recv(1024).decode()
                except OSError:
                    log(self, 'Force closing the connexion with the actual client')
                if not data:
                    log(self, 'Client {} disconnected'.format(str(address)))
                    break
            self.m_client_socket.close()

    def start_server(self):
        log(self, 'Launching the Middleware Websocket Server on {} : {}'.format(str(self.m_ip), str(self.m_port)))
        self.m_thread.start()
        
    def  stop_server(self):
        log(self, 'Stopping the Middleware Websocket Server')
        self.m_is_running = False
        if self.m_client_socket is None:
            log(self, 'Unable to close client connexion : null client socket')
        else:
            self.m_client_socket.close()
        self.m_thread.join()