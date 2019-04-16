#!/usr/local/bin/python3

from enum import Enum
from http.server import HTTPServer

from Utils.OreConstants import AI_PORT, AI_IP
from AI.FearEngine import FearEngine
from Handler.OreHttpRequestHandler import OreHTTPRequestHandler, OreCommandType
from Utils.PacketFactory import PacketFactory

class OnionRingEngineHTTPServer(HTTPServer):
    def __init__(self, ip, port, *args, **kwargs):
        self.m_ip = ip
        self.m_port = port
        self.m_is_server_ready = False
        self.m_is_server_init = False
        self.m_client_ip = None
        self.m_client_port = None

        self.m_fear_engine = FearEngine()
        self.m_fear_engine.train_ia()

        HTTPServer.__init__(self, (self.m_ip, self.m_port), OreHTTPRequestHandler)
        self.start_server()

    def start_server(self):
        print('Launching HTTP server on ' + str(self.m_ip) + ':' + str(self.m_port))
        self.m_is_server_ready = True
        self.serve_forever()

    ### MARK : FearEngine callbacks

    def on_ia_has_predicted(self, status, accuracy, timestamp):
        pass
        #TODO: Send fear_event to midleware

    ### MARK : OreHTTPRequestHandler callbacks

    def on_post_reiceived(self, command, handler, packet=None):
        if command is OreCommandType.INIT:
            if not self.m_is_server_ready:
                handler.send_complete_response(400, PacketFactory.get_program_state_packet(False, 'ORE not ready yet'))
            else:
                packet["client_ip"] = self.m_client_ip
                packet["client_port"] = self.m_client_port
                self.m_is_server_init = True
                handler.send_complete_response(200, PacketFactory.get_program_state_packet(False, 'ORE is ready'))
        elif not self.m_is_server_init:
            handler.send_complete_response(400, PacketFactory.get_program_state_packet(False, 'Server not ready'))
        elif command is OreCommandType.START_AI:
            if not self.m_fear_engine.launch():
                handler.send_complete_response(400, PacketFactory.get_program_state_packet(False, 'AI already launched'))
            else:
                handler.send_complete_response(200, PacketFactory.get_program_state_packet(True, 'Launching Onion Ring Engine AI'))
        elif command is OreCommandType.STOP_AI:
            if not self.m_fear_engine.stop():
                handler.send_complete_response(400, PacketFactory.get_program_state_packet(False, 'AI already stopped'))
            else:
                handler.send_complete_response(200, PacketFactory.get_program_state_packet(True, 'Stopping Onion Ring Engine AI'))
        elif command is OreCommandType.BIOFEEDBACK:
            if not self.m_fear_engine.m_is_running:
                handler.send_complete_response(400, PacketFactory.get_program_state_packet(False, 'Unable to add biofeedback : AI stopped'))
            else:
                self.m_fear_engine.add_bf(packet["bf"], packet["timestamp"], self.on_ia_has_predicted)
                handler.send_complete_response(200, PacketFactory.get_program_state_packet(True, 'Biofeedback added'))


if __name__ == "__main__":
    OnionRingEngineHTTPServer(AI_IP, AI_PORT)