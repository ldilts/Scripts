#!/usr/bin/python

import socket
import sys

class Server:
	'''demonstration class only
		- coded for clarity, not efficiency
	'''
	
	MSGLEN = 16

	def __init__(self, sock=None):
		if sock is None:
			self.sock = socket.socket(
				socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock

	def connect(self, host, port):
		#self.sock.connect((host, port))
		server_address = (host, port)
		print >>sys.stderr, 'starting up on %s port %s' % server_address
		self.sock.bind(server_address)
		self.sock.listen(1)
		
	def loop(self):
		while True:
			# Wait for a connection
			print >>sys.stderr, 'waiting for a connection'
			connection, client_address = self.sock.accept()
			
			try:
				print >>sys.stderr, 'connection from', client_address

				# Receive the data in small chunks and retransmit it
				while True:
					data = connection.recv(16)
					print >>sys.stderr, 'received "%s"' % data
					if data:
						print >>sys.stderr, 'sending data back to the client'
						connection.sendall(data)
					else:
						print >>sys.stderr, 'no more data from', client_address
						break

			finally:
				# Clean up the connection
				connection.close()

# 	def mysend(self, msg, connection):
# 		totalsent = 0
# 		while totalsent < self.MSGLEN:
# 			sent = self.sock.send(msg[totalsent:])
# 			if sent == 0:
# 				raise RuntimeError("socket connection broken")
# 			totalsent = totalsent + sent

	# def myreceive(self, connection):
# 		data = connection.recv(16)
# 		print >>sys.stderr, 'received "%s"' % data
# 		if data:
# 			print >>sys.stderr, 'sending data back to the client'
# 			connection.sendall(data)
# 		else:
# 			print >>sys.stderr, 'no more data from', client_address

a_socket = Server()
a_socket.connect('localhost', 10000)
a_socket.loop()

