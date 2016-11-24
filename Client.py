import socket
import json
import time

"""
MotionControl - MissionControl Socket Client
By Daniel Swoboda (@snoato, swobo.space)
"""

class Client:
	connreq = ' {"ConnREQ" : {"HardwareType" : "Smartphone"} }'
	connstt = ' {"ConnSTT" : {}} '


	def __init__(self, address, port):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		self.sock.connect((address, port))
		self.connect()

	def connect(self):
		self.sock.send(self.connreq)
		resp = self.receive()
		if(resp.keys()[0] == "ConnACK"):
			self.receive()
			self.sock.send(self.connstt)
			print("Connected to Robot")
		else:
			raise Exception()

	def receive(self):
		finished = False
		jsonMsg = None

		counter = 0
		msg = self.sock.recv(2048).decode("utf-8")
		msg = msg.strip(' ')
		if not msg:
			return False
		while not finished:
			try:
				counter += 1
				jsonMsg = json.loads(msg)
				finished = True
			except ValueError:
				if counter > 10:
					return False
				msg1 = self.sock.recv(2048).decode("utf-8")
				msg = msg+msg1

				if not msg1:
					return False
		return json.loads(msg)

	def control_motor(self, lvalue, rvalue):
		if(lvalue == 0):
			lvalue = 1
		else:
			lvalue = lvalue*15
		
		if(rvalue == 0):
			rvalue = 1
		else:
			rvalue = rvalue*15
		
		self.send('{ "Control" : { "Motor Left" : '+str(lvalue)+', "Motor Right" : '+str(rvalue)+' }}')

	def send(self, message):
		print(message)
		self.sock.sendall(message)

