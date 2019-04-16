#!/usr/local/bin/python3

import requests

class OnionRingEngineHTTPSender():

    @staticmethod
    def post_data_to_endpoint(ip, port, rte, data):
        url = 'http://' + ip + ':' + str(port) + rte
        json = data
        try:
            requests.post(url = url, data = data, timeout=0.0000000001) 
        except requests.exceptions.ReadTimeout: 
            pass
