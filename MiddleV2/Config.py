#!/usr/local/bin/python3

from Utils.IpUtils import HostedNetworks

debug = False

# Middleware
MIDDLE_PORT = 8686
ORE_WEBSOCK_PORT = 6666

# Ore
ORE_IP = 'localhost'
ORE_PORT = 8080

# Android
if debug:
	ANDROID_IP = 'localhost'
	ANDROID_PORT = 8282
else:
	ANDROID_IP = HostedNetworks.find_unique_connection()
	ANDROID_PORT = 8080
