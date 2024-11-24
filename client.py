import socket

class Client:

	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
	def connection(self):
		try:
			self.socket.connect((self.host, self.port))
		except:
			return "La clef est corrompue"
	
	def send_data(self, data):
		self.socket.send(data.encode('utf-8'))
		
	def stop(self):
		self.socket.close()
