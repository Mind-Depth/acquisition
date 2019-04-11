#!/usr/local/bin/python3

import socket
import threading
import socketserver
import functools
import sys

sys.path.insert(0, '../')
from Utils.OreConstants import *

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, callback, *args, **keys):
        self.m_callback = callback
        socketserver.StreamRequestHandler.__init__(self, *args, **keys)

    def handle(self):
        #self.request is the TCP socket connected to the client
        self.m_data = self.request.recv(BUFFER_SIZE).strip()
        self.m_callback(self.m_data.decode('utf-8'), self.request, self.client_address)
        #self.request.sendall(self.data.upper())

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class OrEngineServer():

    def __init__(self, ip, port):
        self.m_server = ThreadedTCPServer((ip, port), functools.partial(ThreadedTCPRequestHandler, self.on_command_received))

        self.m_ip, self.m_port = self.m_server.server_address
        server_thread = threading.Thread(target=self.m_server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        self.m_is_running = True
        print('Starting ORE server on ' + self.m_ip + ':' + str(self.m_port) + ' ...')
        while self.m_is_running:
            pass
        self.m_server.shutdown()
        self.m_server.server_close()
        print('Closing ORE server ...')

    def on_command_received(self, data, socket, client_address):
        print('Received following packet from ' + str(client_address) + ' : ' + data)
        if (data == '/kill'):
            socket.sendall(bytes('Server successfuly closed', 'utf-8'))
            self.m_is_running = False


if __name__ == "__main__":
    OrEngineServer(AI_IP, AI_PORT)
