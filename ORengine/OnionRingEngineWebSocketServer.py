#!/usr/local/bin/python3

import threading
import socket
import json

import sys

from Utils.OreConstants import CLIENT_PORT

class OnionRingEngineWebSocketServer():
    def __init__(self, ip):
        self.m_ip = ip
        self.m_port = CLIENT_PORT
        self.m_socket = socket.socket()
        self.m_client_socket = None
        threading.Thread.__init__(self)
        self.m_thread = threading.Thread(target = self.run_serv)


    def run_serv(self):
        self.m_is_running = True
        print('IN SOCKET STARTER\n')
        print('socket args are ip: {}, port {}\n'.format(self.m_ip, self.m_port))
        self.m_socket.bind((self.m_ip, self.m_port))
        while True:
            print('Listen', self.m_ip, self.m_port)
            self.m_socket.listen()
            self.m_client_socket, address = self.m_socket.accept()
            print('Connection from: ' + str(address))
            while True:
                try:
                    data = self.m_client_socket.recv(1024).decode()
                except OSError:
                    print('Force closing the connexion with the actual client')
                if data is None:
                    print('Client ' + str(address) + ' disconnected')
                    break
            self.m_client_socket.close()

    def start_server(self):
        print('Launching the OREngine Websocket Server on ' + str(self.m_ip) + ':' + str(self.m_port) + '...')
        self.m_thread.start()
        

    def  stop_server(self):
        self.m_is_running = False
        if self.m_client_socket is None:
            print('Unable to close client connexion : null client socket')
        else:
            self.m_client_socket.close()
        self.m_thread.join()

    def send_packet_to_client(self, message):
        if self.m_client_socket is None:
            print('Unable to send fear event to the client : null client socket')
        else:
            print('send_packet_to_client', message)
            self.m_client_socket.send(message.encode())
