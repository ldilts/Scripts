#!/usr/bin/python

import socket
import sys
import requests
import json
import datetime
import time
import threading

class Server:
	'''demonstration class only
		- coded for clarity, not efficiency
	'''
	
	# Constants
	MSGLEN = 16
	SERVER_URL = 'https://httpbin.org'
	ID = 12345

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
		
	def loop(self, arg1, stop_event):
		while (not stop_event.is_set()):
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
						# print >>sys.stderr, 'sending data back to the client'
						connection.sendall('ok')

						payload = []
						
						# If open
						if data == '1':
							payload = self.pack_json(True)
						else:
							payload = self.pack_json(False)
							
						self.server_post(payload)
					else:
						print >>sys.stderr, 'no more data from', client_address
						break

			finally:
				# Clean up the connection
				connection.close()
			pass

	# Create JSON file to send to Django				
	def pack_json(self, open):

		# Get current time
		date = datetime.datetime.now()
		
		# Create payload data
		data = [ {
		  "id": self.ID,
		  "open": open,
		  "datetime": {
			"second": date.second,
			"minute": date.minute,
			"hour": date.hour,
			"day": date.day,
			"month": date.month,
			"year": date.year
		  }
		} ]
		
		return json.dumps(data)
				
	def server_post(self, payload):
		r = requests.post(self.SERVER_URL, data = payload)
		print "Status: ", r.status_code

	def get_stuff(self, arg1, stop_event):
		while (not stop_event.is_set()):
			r = requests.get(self.SERVER_URL)
			decoded = json.loads(r.text)
			print >>sys.stderr, 'Got "%s"\n' % decoded
			time.sleep(5)
			pass

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

while True:
	a_socket = Server()
	a_socket.connect('localhost', 10500)

	threads = [] 

	t1_stop = threading.Event()
	t1 = threading.Thread(target = a_socket.loop, args=(1, t1_stop))

	t2_stop = threading.Event()
	t2 = threading.Thread(target = a_socket.get_stuff, args=(2, t2_stop))

	t1.setDaemon(True)
	t2.setDaemon(True)

	threads.append(t1)
	threads.append(t2)

	t1.start()
	t2.start()

	for x in threads: 
		x.join()
		
	print "Done"
