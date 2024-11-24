#!/usr/bin/env python3
# coding: utf-8
 
import socket 


class MySocket:
	
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.port = 5000
		self.sock.timeout(0)
		try:
			self.sock.connect('10.254.254.254', '1')
			self.host = self.sock.getsockname()[0]
		except Exception as e:
			self.host = "Erreur:" +str(e)
		else:
			self.sock.bind((self.host, self.port))
			
	def start(self):
		while True:
			self.sock.listen(5)
			client, address = self.sock.accept()
			print("{} connected".format(address))
			
			response = client.recv(255)
			if response != "":
				print(response
	def closeSock(self):
		print("close")
		client.close()
		self.sock.close()

if __name__ == "__main__":
	serveur_sock = MySocket()
	serveur_sock.start()
