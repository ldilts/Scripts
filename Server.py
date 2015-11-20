#!/usr/bin/python

import socket
import sys

class Server:
	'''demonstration class only
		- coded for clarity, not efficiency
	'''

	def __init__(self, sock=None):
		print "In init"
		if sock is None:
			self.sock = socket.socket(
				socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock

	def connect(self, host, port):
		print "In connect"
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

	def mysend(self, msg):
		totalsent = 0
		while totalsent < MSGLEN:
			sent = self.sock.send(msg[totalsent:])
			if sent == 0:
				raise RuntimeError("socket connection broken")
			totalsent = totalsent + sent

	def myreceive(self):
		print "In receive"
		chunks = []
		bytes_recd = 0
		while bytes_recd < MSGLEN:
			chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
			if chunk == '':
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			bytes_recd = bytes_recd + len(chunk)
		return ''.join(chunks)

a_socket = Server()
a_socket.connect('localhost', 10000)
print "back!"
a_socket.loop()

