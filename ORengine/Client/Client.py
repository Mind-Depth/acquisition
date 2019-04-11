#!/usr/local/bin/python3

import socket
import sys
sys.path.insert(0, '../')

from Utils.OreConstants import *

def client(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    print('Connected to ' + ip + ':' + str(port))
    m_is_running = True
    while m_is_running:
        line = sys.stdin.readline()
        
        if (line.strip('\n') == '/quit'):
            m_is_running = False
        else:
            sock.sendall(bytes(line, 'utf-8'))
            response = str(sock.recv(BUFFER_SIZE), 'utf-8')
            if (response != ''):
                print("Received: {}".format(response))
    sock.close()
    print('Closing ORE client...')

if __name__ == "__main__":
    client(AI_IP, AI_PORT)