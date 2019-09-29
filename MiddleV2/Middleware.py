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

from Server.MiddlewareHttpServer import MiddlewareHttpServer
from Server.MiddlewareWebsocketServer import MiddlewareWebsocketServer
from Utils.PrintUtils import log
from Keyboard.KeyboardController import KeyboardController
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import requests
import json
import sys

class MiddlewareHttpController():
    def  __init__(self):
        self.packet_callbacks = {}

    def post_data_to_endpoint(self, data, url):
        try:
            log(self, 'Sending {} to {}'.format(data, url))
            session = requests.Session()
            session.trust_env = False
            response = session.post(url = url, headers = self.get_header, data = data, timeout=10) 
        except requests.exceptions.ReadTimeout:
            pass

    def get_header(self):
        return {
            'Content-Type': 'application/json'
        }

class Middleware():

    def __init__(self, ore_ip, ore_port, android_ip, android_port):
        self.m_keyboard_factory = {
            'start': self.start_session,
            'stop': self.stop_session
        }

        self.m_middleware_http_sender = MiddlewareHttpController()
        self.m_websocket_server = MiddlewareWebsocketServer(ore_ip, ore_port + 1)
        self.m_websocket_server.start_server()
        self.m_keyboard_controller = KeyboardController(self.keyboard_callback)
        self.m_keyboard_controller.start()

        # TODO : Init named pipe unit here

    def shutdown_middleware(self):
        self.m_websocket_server.stop_server()
        self.m_keyboard_controller.stop()

    ###
    # Callbacks from KeyboardController
    ###

    def keyboard_callback(self, key):
        try:
            self.m_keyboard_factory[key]()
        except KeyError:
            log(self, 'The input is not valid')

    def start_session(self):
        log(self, 'Starting session')
        # TODO : Send INIT to ore and Android

    def stop_session(self):
        log(self, 'Stopping session')

if __name__ == "__main__":
    Middleware(ore_ip='localhost', ore_port=8484, android_ip='localhost', android_port=4242)