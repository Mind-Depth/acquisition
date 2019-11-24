#!/usr/local/bin/python3

from Server.MiddlewareHandler import MiddlewareHttpHandler
from Utils.PacketFactory import PacketFactory
from Utils.PrintUtils import log
from http.server import HTTPServer
from socketserver import ThreadingMixIn
import threading
import json

class MiddlewareHttpServer(ThreadingMixIn, HTTPServer):
    def __init__(self, ip, port, bf_callback):
        self.m_ip = ip
        self.m_port = port
        self.m_bf_callback = bf_callback
        ThreadingMixIn.__init__(self)
        HTTPServer.__init__(self, (self.m_ip, self.m_port), MiddlewareHttpHandler)

        self.m_thread = threading.Thread(target = self.run_server)

    def run_server(self):
        try:
            self.serve_forever()
        except:
            pass
        log(self, 'Aborting')
        self.abort()

    def start_server(self, abort):
        log(self, 'Launching HTTP server on {} : {}'.format(self.m_ip, self.m_port))
        self.abort = abort
        self.m_thread.start()

    def stop_server(self):
        log(self, 'Stopping MiddlewareHttpServer')
        self.m_thread.terminate()

    ###
    # Callbacks from MiddlewareHandler
    ###

    def on_packet_received(self, packet, handler):
        try:
            log(self, 'Packet {} received from {}'.format(packet['message_type'], handler.client_address))
            if packet['message_type'] ==  "BIOFEEDBACK":
                self.m_bf_callback(packet['bf'], packet['timestamp'])
                handler.send_complete_response(200, json.dumps(PacketFactory.get_program_state_packet(True, "BF received")))
        except json.decoder.JSONDecodeError:
            print('ERROR: Unable to parse the current Json : ' + str(packet))
            handler.send_complete_response(400, json.dumps(PacketFactory.get_program_state_packet(False, "Bad format")))