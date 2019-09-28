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

from MiddlewareHandler import MiddlewareHttpHandler
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import requests
import json

class MiddlewareHttpController():
    def  __init__(self):
        self.packet_callbacks = {}

    def post_data_to_endpoint(self, data, url):
        try:
            print('Sending ' + data + ' to ' + url)
            session = requests.Session()
            session.trust_env = False
            response = session.post(url = url, headers = self.get_header, data = data, timeout=10) 
        except requests.exceptions.ReadTimeout:
            pass

    def get_header(self):
        return {
            'Content-Type':  'application/json'
        }

class MiddlewareHttpServer(ThreadingMixIn, HTTPServer):
    def __init__(self, ip, port):
        self.m_ip = ip
        self.m_port = port

        ThreadingMixIn.__init__(self)
        HTTPServer.__init__(self, (self.m_ip, self.m_port), MiddlewareHttpHandler)

        self.start_server()

    def start_server(self):
        print('Launching HTTP server on ' + str(self.m_ip) + ':' + str(self.m_port))
        self.serve_forever()

class Middleware():

    def __init__(self, ip, port):
        fear_event_http_server = MiddlewareHttpServer(ip, port)
        # TODO : Launch websocket serv
        # TODO : Launch named pipe unit
        # TODO : INIT ore and Android

if __name__ == "__main__":
    Middleware('localhost', 8484)