#!/usr/local/bin/python3

from Utils.PrintUtils import log
import threading
import requests
import json

class MiddlewareHttpController():
    def  __init__(self):
        self.packet_callbacks = {}

    def post_data_to_endpoint(self, data, url):
        new_thread = threading.Thread(target = self.post, args = (data, url))
        new_thread.start()

    def get_header(self):
        return {
            'Content-Type': 'application/json'
        }

    def post(self, data, url):
        try:
            log(self, 'Sending {} to {}'.format(data, url))
            session = requests.Session()
            session.trust_env = False
            response = session.post(url = url, headers = self.get_header(), data = data, timeout=2) 
        except requests.exceptions.ReadTimeout:
            log(self, 'Timed out')
        except requests.exceptions.ConnectionError:
            log(self, 'Connection refused')