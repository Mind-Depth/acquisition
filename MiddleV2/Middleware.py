#!/usr/local/bin/python3

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
from enum import Enum
import sys

class ClientType(Enum):
    DEVICE = 0,
    ORE = 1

class Middleware():

    def __init__(self, ore_ip, ore_port, android_ip, android_port):
        self.m_keyboard_factory = {
            'init': self.init_session,
            'start': self.start_session,
            'stop': self.stop_session,
            'init_ore': self.init_ore,
            'init_android': self.init_android,
            'start_ore': self.start_ore,
            'start_android': self.start_android,
            'stop_ore': self.stop_ore,
            'stop_android': self.stop_android
        }

        self.m_packets_factory = {
            "INIT": self.on_init_packet_response_received,
            "CONTROL_SESSION": self.on_control_session_packet_received,
        }

        self.m_ore_ready = False
        self.m_android_ready = False

        self.m_ip = 'localhost'
        #self.m_ip = get_ip()
        self.m_port = MIDDLE_PORT
        self.m_websock_port = MIDDLE_WEBSOCK_PORT

        self.m_ore_ip = ore_ip
        self.m_ore_port = ore_port
        self.m_ore_rte = '/server'
        self.m_android_ip = android_ip
        self.m_android_port = android_port
        self.m_android_rte = '/android'

        self.m_middleware_http_server = MiddlewareHttpServer(self.m_ip, self.m_port, self.on_biofeedback_packet_received)
        self.m_middleware_http_server.start_server()
        self.m_middleware_http_sender = MiddlewareHttpController(self.m_packets_factory)
        self.m_websocket_server = MiddlewareWebsocketServer(self.m_ip, self.m_websock_port, self.on_fear_event_received)
        self.m_keyboard_controller = KeyboardController(self.m_keyboard_factory)
        self.m_keyboard_controller.start()
        # TODO : INIT NAMEDPIPECONTROLLER HERE

    def shutdown_middleware(self):
        self.m_websocket_server.stop_server()
        self.m_keyboard_controller.stop()

    def get_ore_endpoint(self):
        return 'http://{}:{}/'.format(self.m_ore_ip, self.m_ore_port)

    def get_android_endpoint(self):
        return 'http://{}:{}/'.format(self.m_android_ip, self.m_android_port)

    ###
    # Callbacks from NamedPipeController
    ###

    def on_init_packet_received(self):
        pass

    def on_control_session_packed_received(self):
        pass

    ###
    # Callbacks from MiddlewareHttpController
    ###

    def on_init_packet_response_received(self, packet, url):
        log(self, 'on_init_packet_response_received')
        if packet['status']:
            if url == self.get_ore_endpoint() and not self.m_ore_ready:
                log(self, 'ORE successfuly init')
                self.m_ore_ready = True
                self.m_websocket_server.connect_to_ore()
                self.m_websocket_server.start_mws()
            elif url == self.get_android_endpoint() and not self.m_android_ready:
                log(self, 'Android successfuly init')
                self.m_android_ready = True
        else:
            log(self, 'Unable to init the target')

    def on_control_session_packet_received(self, packet, url):
        log(self, 'on_control_session_packet_received')
        if packet['status']:
            if url == self.get_ore_endpoint():
                log(self, 'ORE successfuly launched')
            elif url == self.get_android_endpoint():
                log(self, 'Android successfuly launched')
        else:
            log(self, 'Unable to start the target')

    ###
    # Callbacks from MiddlewareHttpServer
    ###

    def on_biofeedback_packet_received(self, bf, timestamp):
        log(self, 'Biofeedback received with values bpm {} ts {}'.format(bf, timestamp))
        self.m_middleware_http_sender.post_data_to_endpoint(PacketFactory.get_biofeedback_packet(bf, timestamp), self.get_ore_endpoint())

    ###
    # Callbacks from MiddlewareHttpServer
    ###

    def on_fear_event_received(self, packet):
        log(self, 'New FearEvent {} received. Transmitting to generation...'.format(packet))
        #  TODO : TRANSMIT DATA TO GENERATION VIA NAMEDPIPECONTROLLER

    ###
    # Callbacks from KeyboardController
    ###

    def init_session(self):
        log(self, 'Init session')
        if not self.m_ore_ready and not self.m_android_ready:
            self.init_ore()
            self.init_android()
        else:
            log(self, 'Error ORE or Android already ready')

    def start_session(self):
        log(self, 'Starting session')
        if self.m_ore_ready and self.m_android_ready:
            self.start_ore()
            self.start_android()
        else:
            log(self, 'Error ORE or Android not ready')

    def stop_session(self):
        log(self, 'Stopping session')
        self.stop_ore()
        self.stop_android()

    def init_ore(self):
        log(self, 'Init ORE...')
        self.m_middleware_http_sender.post_data_to_endpoint(PacketFactory.get_init_packet(self.m_ip, self.m_port, self.m_ore_rte), self.get_ore_endpoint())

    def init_android(self):
        log(self, 'Init Android...')
        self.m_middleware_http_sender.post_data_to_endpoint(PacketFactory.get_init_packet(self.m_ip, self.m_port, self.m_android_rte), self.get_android_endpoint())

    def start_ore(self):
        log(self, 'Starting ORE...')
        if self.m_ore_ready:
            self.m_middleware_http_sender.post_data_to_endpoint(PacketFactory.get_control_session_packet(True), self.get_ore_endpoint())
        else:
            log(self, 'Error ORE not ready')

    def start_android(self):
        log(self, 'Starting Android...')
        if self.m_android_ready:
            self.m_middleware_http_sender.post_data_to_endpoint(PacketFactory.get_control_session_packet(True), self.get_android_endpoint())
        else:
            log(self, 'Error Android not ready')

    def stop_ore(self):
        log(self, 'Stopping ORE...')
        self.m_middleware_http_sender.post_data_to_endpoint(PacketFactory.get_control_session_packet(False), self.get_ore_endpoint())

    def stop_android(self):
        log(self, 'Stopping Android...')
        self.m_middleware_http_sender.post_data_to_endpoint(PacketFactory.get_control_session_packet(False), self.get_android_endpoint())

if __name__ == "__main__":
    Middleware(ore_ip=ORE_IP, ore_port=ORE_PORT, android_ip=ANDROID_IP, android_port=ANDROID_PORT)