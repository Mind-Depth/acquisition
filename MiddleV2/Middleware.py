#!/usr/local/bin/python3

# TODO : LAUNCH SERVER FOR ORE
# TODO : OPEN NAMED PIPE FOR GEN
# TODO : NAMED PIPE <- INIT
# TODO : SEND INIT TO ORE && ACQUI
# TODO : PROGRAM_STATE TRUE FROM ORE && ACQUI
# TODO : PROGRAM_STATE TRUE TO GEN VIA NAMED PIPE
# TODO : NAMED PIPE <- CONTROL_SESSION TRUE
# TODO : SEND CONTROL_SESSION TRUE TO ORE && ACQUI
# TODO : PROGRAM_STATE TRUE FROM ORE && ACQUI
# TODO : WHEN BF FROM ACQUI -> SEND TO ORE
# TODO : WHEN FEAR_EVENT FROM ORE -> SEND TO GEN VIA NAMED PIPE
# TODO : NAMED PIPE <- CONTROL_SESSION FALSE
# TODO : SEND CONTROL_SESSION FALSE TO ORE && ACQUI
# TODO : PROGRAM_STATE TRUE FROM ORE && ACQUI
# TODO : EXIT

from Servers.MiddlewareHttpServer import MiddlewareHttpServer
from Servers.MiddlewareWebsocketServer import MiddlewareWebsocketServer
from Utils.PrintUtils import log
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import requests
import json

class MiddlewareHttpController():
    def  __init__(self):
        self.packet_callbacks = {}

    def post_data_to_endpoint(self, data, url):
        try:
            log(self, 'Sending {} to {}'.format(data, url))
            print()
            session = requests.Session()
            session.trust_env = False
            response = session.post(url = url, headers = self.get_header, data = data, timeout=10) 
        except requests.exceptions.ReadTimeout:
            pass

    def get_header(self):
        return {
            'Content-Type':  'application/json'
        }

class Middleware():

    def __init__(self, ip, port):
        self.m_http_server = MiddlewareHttpServer(ip, port)
        self.m_http_server.start_server()
        self.m_websocket_server = MiddlewareWebsocketServer(ip, port + 1)
        self.m_websocket_server.start_server()
        # TODO : Init named pipe unit here
        # TODO : INIT ore and Android

    def shutdown_servers(self):
        self.m_http_server.stop_server()
        self.m_websocket.stop_server()

if __name__ == "__main__":
    Middleware('localhost', 8484)