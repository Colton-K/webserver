#!/usr/bin/env python3
#
# TP-Link Wi-Fi Smart Plug Protocol Client
# For use with TP-Link HS-100 or HS-110
#
# by Lubomir Stroetmann
# Copyright 2016 softScheck GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys
import socket
from struct import pack

version = 0.3

# Check if hostname is valid
def validHostname(hostname):
	try:
		socket.gethostbyname(hostname)
	except socket.error:
		parser.error("Invalid hostname.")
	return hostname

# Check if port is valid
def validPort(port):
        try:
            port = int(port)
        except ValueError:
            parser.error("Invalid port number.")

        if ((port <= 1024) or (port >65535)) :
            parser.error("Invalid port number.")

        return port


# Predefined Smart Plug Commands
# For a full list of commands, consult tplink_commands.txt
commands = {		'info'     : '{"system":{"get_sysinfo":{}}}',
			'on'       : '{"system":{"set_relay_state":{"state":1}}}',
			'off'      : '{"system":{"set_relay_state":{"state":0}}}',
	    		'ledoff'   : '{"system":{"set_led_off":{"off":1}}}',
			'ledon'    : '{"system":{"set_led_off":{"off":0}}}',
			'cloudinfo': '{"cnCloud":{"get_info":{}}}',
			'wlanscan' : '{"netif":{"get_scaninfo":{"refresh":0}}}',
			'time'     : '{"time":{"get_time":{}}}',
			'schedule' : '{"schedule":{"get_rules":{}}}',
			'countdown': '{"count_down":{"get_rules":{}}}',
			'antitheft': '{"anti_theft":{"get_rules":{}}}',
			'reboot'   : '{"system":{"reboot":{"delay":1}}}',
			'reset'    : '{"system":{"reset":{"delay":1}}}',
			'energy'   : '{"emeter":{"get_realtime":{}}}'
}

# Encryption and Decryption of TP-Link Smart Home Protocol
# XOR Autokey Cipher with starting key = 171
# Python 3.x Version
def encrypt(string):
	key = 171
	result = pack('>I', len(string))
	for i in string:
		a = key ^ ord(i)
		key = a
		result += bytes([a])
	return result

def decrypt(string):
	key = 171
	result = ""
	for i in string:
		a = key ^ i
		key = i
		result += chr(a)
	return result

# Send command and receive reply
def sendCommand(ip, port, command):
	cmd = commands[command]
	try:
		sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# sock_tcp.settimeout(int(args.timeout))
		sock_tcp.settimeout(10)
		sock_tcp.connect((ip, port))
		sock_tcp.settimeout(None)
		sock_tcp.send(encrypt(cmd))
		data = sock_tcp.recv(2048)
		sock_tcp.close()

		decrypted = decrypt(data[4:])

		# if args.quiet:
			# print(decrypted)
		# else:
		print("Sent:     ", cmd)
		print("Received: ", decrypted)

	except socket.error:
		quit("Could not connect to host " + ip + ":" + str(port))

	return decrypted