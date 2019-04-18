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
        
    """
        INIT
        `{"message_type": "INIT", "client_ip": "190.262.15.3", "client_port": 8080, "client_rte":"/server"}`

        CONTROL SESSION
        `{"message_type": "CONTROL_SESSION", "status": true}`

        FEAR EVENT
        `{"message_type": "FEAR_EVENT", "status_fear": true, "fear_accuracy": 0.0, "timestamp": 1234532}`

        PROGRAM STATE
        `{"message_type": "PROGRAM_STATE", "status": false, "message": "Ca marche pas"}`

        BIOFEEDBACK
        `{"message_type": "BIOFEEDBACK", "bf": 55, "timestamp": 14323553}`
    """


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
        print('in android_program_state')

    def android_biofeedback(self, payload):
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
        print('in android_biofeedback')

    def ai_fear_event(self, payload):
        print('in android_biofeedback')

def main():
    server = Server()
    server._start()

if __name__ == "__main__":
    main()
