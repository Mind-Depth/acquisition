#!/usr/bin/env python3

'''
    On doit recup l'adresse ip locale d'alex en 3eme param et la set dans la classe Config
    On a des handlers http pour ben et alex dans 2 classes et on passe des callbacks pour gérer les echanges de data
    On a un thread a part qui parle a chicha en permanence
'''

import os
import bottle
from Requestor import Requestor
from Config import Config

class Server():

    def get_android_message_dict(self):
        return {
            'PROGRAM_STATE': self.android_program_state,
            'BIOFEEDBACK': self.android_biofeedback,
        }


    def get_ai_message_dict(self):
        return {
            'FEAR_EVENT': self.ai_fear_event,
            'PROGRAM_STATE': self.ai_program_state,
        }

    def __init__(self, host='localhost', port=8080):
        self.m_host = host
        self.m_port = port
        self.m_app = bottle.Bottle()
        self.m_requestor = Requestor()
        self.m_config = Config()
        self.m_ai_message_dict = self.get_ai_message_dict()
        self.m_android_message_dict = self.get_android_message_dict()
        self._route()

    def _route(self):
        self.m_app.route('/android', method="POST", callback=self.handler_android)
        self.m_app.route('/server', method="POST", callback=self.handler_ai)

    def _start(self):
        self.m_app.run(host=self.m_host, port=self.m_port)

    def _stop(self):
        # coder les envoies de requetes + sur le pipe disant qu'on stop le server
        #a trouver mieux
        exit(0)
        
    #
    # ANDROID HANDLERS
    #

    def handler_android(self):
        try:
            if 'message_type' in bottle.request.json:
                self.m_android_message_dict[bottle.request.json['message_type']](bottle.request.json)
        except:
            print('ERROR IN HANDLER_ANDROID')
            # gérer le cas

    def android_program_state(self, payload):
        try:
            if payload['status'] != True:
                # TODO dire a chicha qu'il y a erreur coté android et stop, bien utiliser payload['message']
                self.m_requestor.start_request('CONTROL_SESSION', status=False, address=self.m_config.m_ai_address)
        except Exception as e:
            print(e)
        print('in android_program_state')

    def android_biofeedback(self, payload):
        try:
            if payload['bf'] != 0:
                self.m_requestor.start_request('BIOFEEDBACK', biofeedback=payload['bf'], timestamp=payload['timestamp'], address=self.m_config.m_ai_address)
        except Exception as e:
            print(e)
        print('in android_biofeedback')


    #
    # AI HANDLERS
    #

    def handler_ai(self):
        try:
            if 'message_type' in bottle.request.json:
                self.m_ai_message_type[bottle.request.json['message_type']](bottle.request.json)
        except:
            print('ERROR IN HANDLER_AI')
            # gérer le cas

    def ai_program_state(self, payload):
        # this is web socket handled
        print('in android_biofeedback')

    def ai_fear_event(self, payload):
        # this is web socket handled
        print('in android_biofeedback')

def main():
    server = Server()
    server._start()

if __name__ == "__main__":
    main()
