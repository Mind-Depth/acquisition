#!/usr/local/bin/python3

from Server.MiddlewareHandler import MiddlewareHttpHandler
from Utils.PrintUtils import log
from http.server import HTTPServer
from socketserver import ThreadingMixIn
import threading

class MiddlewareHttpServer(ThreadingMixIn, HTTPServer):
    def __init__(self, ip, port):
        self.m_ip = ip
        self.m_port = port
        ThreadingMixIn.__init__(self)
        HTTPServer.__init__(self, (self.m_ip, self.m_port), MiddlewareHttpHandler)

        self.m_thread = threading.Thread(target = self.run_server)

    def run_server(self):
        log(self, 'Launching HTTP server on {} : {}'.format(self.m_ip, self.m_port))
        self.serve_forever()

    def start_server(self):
        log(self, 'Starting MiddlewareHttpServer')
        self.m_thread.start()

    def stop_server(self):
        log(self, 'Stopping MiddlewareHttpServer')
        self.m_thread.terminate()