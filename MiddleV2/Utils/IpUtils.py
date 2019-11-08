#!/usr/local/bin/python3

import socket

def get_ip():
    return socket.gethostbyname(socket.gethostname()) 