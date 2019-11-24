#!/usr/local/bin/python3

import socket
import ipaddress
from subprocess import check_output
from xml.etree.ElementTree import fromstring

def get_ip():
    return socket.gethostbyname(socket.gethostname()) 

class HostedNetworks:

	NIC_PROPERTIES = ['Description', 'IPAddress', 'IPSubnet', 'DHCPEnabled']
	NIC_FILTERS = {'DHCPEnabled': False, 'IPEnabled': True}

	@classmethod
	def fetch_wmic_nic_interfaces(cls):
		where = ' And '.join(f'{key}={repr(value)}' for key, value in cls.NIC_FILTERS.items())
		where = where and f' where "{where}"'
		cmd = 'wmic.exe nicconfig' + where + ' get ' + ', '.join(cls.NIC_PROPERTIES) + ' /format:rawxml'
		xml = fromstring(check_output(cmd))
		interfaces = {}
		for node in xml.findall('./RESULTS/CIM/INSTANCE'):
			properties = {}
			for property in node:
				name = property.attrib['NAME']
				if property.tag == 'PROPERTY':
					properties[name] = property.find('./VALUE').text
				elif property.tag == 'PROPERTY.ARRAY':
					properties[name] = [value.text for value in property.findall('./VALUE.ARRAY/VALUE')]
			ipv4, ipv6 = properties['IPAddress']
			subnet, mask = properties['IPSubnet']
			interfaces[ipv4] = dict(
				desc = properties['Description'],
				network = ipaddress.ip_network(f'{ipv4}/{subnet}', strict=False)
			)
		return interfaces

	@staticmethod
	def fetch_arp_interfaces():
		interfaces = {}
		for entry in check_output('arp -a').decode().split('\r\n\r\n'):
			header, table, *addresses = entry.strip().split('\r\n')
			prompt, ip, *meta = header.split()
			iaddrs = []
			for address in addresses:
				iaddr, paddr, etype = address.split()
				iaddrs.append(ipaddress.ip_address(iaddr))
			interfaces[ip] = iaddrs
		return interfaces

	@classmethod
	def iter_connections(cls):
		nics = cls.fetch_wmic_nic_interfaces()
		arps = cls.fetch_arp_interfaces()
		for ip in nics.keys() & arps.keys():
			properties = nics[ip]
			network = properties['network']
			blacklist = [network.network_address, network.broadcast_address]
			connections = []
			for addr in arps[ip]:
				if addr in network and not addr in blacklist:
					connections.append(str(addr))
			if connections:
				yield properties['desc'], connections

	@classmethod
	def find_unique_connection(cls):
		(interface, (ip,)), = cls.iter_connections()
		return ip