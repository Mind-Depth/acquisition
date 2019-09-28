#!/usr/local/bin/python3

AI_IP = 'localhost'
AI_PORT = 4242

import random
import os

port_path = r'Utils\port.txt'
if os.path.isfile(port_path):

    with open(port_path, 'r') as f:
        CLIENT_PORT = int(f.read())

else:

    CLIENT_PORT = 6666 + random.randint(0, 42)
    with open(port_path, 'w') as f:
        f.write(str(CLIENT_PORT))

