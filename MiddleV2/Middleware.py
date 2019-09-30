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

from Server.MiddlewareHttpController import MiddlewareHttpController
from Server.MiddlewareHttpServer import MiddlewareHttpServer
from Server.MiddlewareWebsocketServer import MiddlewareWebsocketServer
from Utils.PrintUtils import log
from Utils.PacketFactory import PacketFactory
from Utils.IpUtils import get_ip
from Keyboard.KeyboardController import KeyboardController
from Config import *
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import sys

class Middleware():

    def __init__(self, ore_ip, ore_port, android_ip, android_port):
        self.m_keyboard_factory = {
            'start': self.start_session,
            'stop': self.stop_session
        }

        self.m_ip = 'localhost'
        #self.m_ip = get_ip()
        self.m_port = MIDDLE_PORT

        self.m_ore_ip = ore_ip
        self.m_ore_port = ore_port
        self.m_ore_rte = '/server'
        self.m_android_ip = android_ip
        self.m_android_port = android_port
        self.m_android_rte = '/android'

        self.m_middleware_http_sender = MiddlewareHttpController()
        self.m_websocket_server = MiddlewareWebsocketServer(self.m_ip, self.m_port)
        self.m_websocket_server.start_server()
        self.m_keyboard_controller = KeyboardController(self.m_keyboard_factory)
        self.m_keyboard_controller.start()
        # TODO : Init named pipe unit here

    def shutdown_middleware(self):
        self.m_websocket_server.stop_server()
        self.m_keyboard_controller.stop()

    ###
    # Callbacks from KeyboardController
    ###

    def start_session(self):
        log(self, 'Starting session')
        self.m_middleware_http_sender.post_data_to_endpoint(PacketFactory.get_init_json(self.m_ip, self.m_port, self.m_ore_rte), 'http://{}:{}'.format(self.m_ore_ip, self.m_ore_port))
        self.m_middleware_http_sender.post_data_to_endpoint(PacketFactory.get_init_json(self.m_ip, self.m_port, self.m_android_rte), 'http://{}:{}'.format(self.m_android_ip, self.m_android_port))

    def stop_session(self):
        log(self, 'Stopping session')

if __name__ == "__main__":
    Middleware(ore_ip=ORE_IP, ore_port=ORE_PORT, android_ip=ANDROID_IP, android_port=ANDROID_PORT)