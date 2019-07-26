#!/usr/local/bin/python3

from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import json

class AwesomeHttpRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.request_callbacks = {
            "PROGRAM_STATE": self.on_program_state_packet_received,
            "BIOFEEDBACK": self.onHReqReceived
        }

        super().__init__(*args, directory="Harvester/", **kwargs)
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        try:
            jsonPacket = PacketFactory.get_json_from_packet(body)
            self.request_callbacks[jsonPacket["message_type"]](jsonPacket)
        except json.decoder.JSONDecodeError:
            print('ERROR: Unable to parse the current Json : ' + str(body))
            self.send_complete_response(400, PacketFactory.get_program_state_json(False, 'Unable to parse the current Json'))

    def on_program_state_packet_received(self, packet):
        pass

    def on_biofeedback_packet_received(self, packet):
        pass

class AwesomeHttpServer(HTTPServer):
    def __init__(self, ip, port):
        self.m_ip = ip
        self.m_port = port

        HTTPServer.__init__(self, (self.m_ip, self.m_port), AwesomeHttpRequestHandler)
        self.start_server()

if __name__ == "__main__":
    pass