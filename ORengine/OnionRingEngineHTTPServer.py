#!/usr/bin/env python3

from enum import Enum
from http.server import HTTPServer

import sys

old_write = sys.stdout.write
def _write(*args, **kwargs):
    old_write(*args, **kwargs)
    sys.stdout.flush()
sys.stdout.write = _write

from Utils.OreConstants import AI_PORT, AI_IP
from AI.FearEngine import FearEngine
from Handler.OreHttpRequestHandler import OreHTTPRequestHandler, OreCommandType
from Utils.PacketFactory import PacketFactory
from OnionRingEngineWebSocketServer import OnionRingEngineWebSocketServer

class OnionRingEngineHTTPServer(HTTPServer):
    def __init__(self, ip, port, *args, **kwargs):
        self.m_ip = ip
        self.m_port = port
        self.m_is_server_ready = False
        self.m_is_server_init = False
        self.m_socket_server = OnionRingEngineWebSocketServer(self.m_ip)
        self.m_fear_engine = FearEngine()
        self.m_fear_engine.train_ia()

        HTTPServer.__init__(self, (self.m_ip, self.m_port), OreHTTPRequestHandler)
        self.start_server()

    def start_server(self):
        print('Launching HTTP server on ' + str(self.m_ip) + ':' + str(self.m_port))
        self.m_is_server_ready = True
        self.serve_forever()

    def start_websocket_server(self):
        self.m_socket_server.start_server()

    def stop_websocket_server(self):
        self.m_socket_server.stop_server()

    def on_init_command_received(self, handler, packet):
        if not self.m_is_server_ready:
            handler.send_complete_response(400, PacketFactory.get_program_state_json(False, 'ORE not ready yet'))
        elif self.m_is_server_init:
            handler.send_complete_response(200, PacketFactory.get_program_state_json(False, 'ORE already init'))
        else:
            self.m_is_server_init = True
            self.start_websocket_server()
            handler.send_complete_response(200, PacketFactory.get_program_state_json(True, 'ORE is ready'))

    def on_start_command_received(self, handler, packet):
        if not self.m_fear_engine.launch():# TODO False
            handler.send_complete_response(200, PacketFactory.get_program_state_json(True, 'AI already launched'))
        else:
            handler.send_complete_response(200, PacketFactory.get_program_state_json(True, 'Launching Onion Ring Engine AI'))

    def on_stop_command_received(self, handler, packet):
        if not self.m_fear_engine.stop(): # TODO False
            handler.send_complete_response(200, PacketFactory.get_program_state_json(True, 'AI already stopped'))
        else:
            self.stop_websocket_server()
            handler.send_complete_response(200, PacketFactory.get_program_state_json(True, 'Stopping Onion Ring Engine AI'))

    def on_bio_packet_received(self, handler, packet):
        if not self.m_fear_engine.m_is_running:
            handler.send_complete_response(400, PacketFactory.get_program_state_json(False, 'Unable to add biofeedback : AI stopped'))
        else:
            self.m_fear_engine.add_bf(packet["bf"], packet["timestamp"], self.on_ia_has_predicted)
            handler.send_complete_response(200, PacketFactory.get_program_state_json(True, 'Biofeedback added'))

    ### MARK : FearEngine callbacks

    def on_ia_has_predicted(self, status, accuracy, timestamp):
        print('on_ia_has_predicted', status, accuracy, timestamp)
        self.m_socket_server.send_packet_to_client(PacketFactory.get_fear_event_json(status, accuracy, timestamp))

    ### MARK : OreHTTPRequestHandler callbacks

    def on_post_reiceived(self, command, handler, packet=None):
        if command is OreCommandType.INIT:
            self.on_init_command_received(handler, packet)
        elif not self.m_is_server_init:
            handler.send_complete_response(400, PacketFactory.get_program_state_json(False, 'Server not ready'))
        elif command is OreCommandType.START_AI:
            self.on_start_command_received(handler, packet)
        elif command is OreCommandType.STOP_AI:
            self.on_stop_command_received(handler, packet)
        elif command is OreCommandType.BIOFEEDBACK:
            self.on_bio_packet_received(handler, packet)

if __name__ == "__main__":
    OnionRingEngineHTTPServer(AI_IP, AI_PORT)