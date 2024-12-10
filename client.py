import socket
import threading
import Interface

class MyClient:

	def __init__(self, username : str, ip : str):
		self.username = username
		self.ip = ip
		self.to_send = None
		
	def receive_messages(self, client_socket):
    		while True:
        		try:
            			message = client_socket.recv(1024).decode('utf-8')
            			if message:
            				if message.split("$")[0] == "CCUP":
            					self.to_send = []
            					self.to_send.append(choix de cupidon) # a modifier je sais pas comment récup le choix
            					"""
            						Pour Victor : dans linstruction précédente, je dois pouvoir récupérer les choix fais pas l'utilisateurs.
            					"""
            				elif message.split("$")[0] == "CVOL":
            					self.to_send = Interface.action #a modifier avec Victor
            					#changer image
            				elif message.split("$")[0] == "VLOU":
            					self.to_send = Interface.action #a modifier avec Victor
            				elif message.split("$")[0] == "CVOY":
            					self.to_send = Interface.action #a modifier avec Victor	
            				elif message.split("$")[0] == "CVOY":
            					#a voir si vraiment util
            					print(f"{message[message.index('$')+1:]}")
            				elif message.split("$")[0] == "CORSA":
            					print(message.split("$")[1])
            					self.to_send = Interface.action
            				elif message.split("$")[0] == "CSORST":
            					self.to_send = Interface.action #Selection du gros fils de pute à tuer
            				elif message.split("$")[0] == "CSORS":
            					self.to_send = Interface.action #Selection du mec qui se prend pour Jésus
            				elif message.split("$")[0] == "VOTE":
            					self.to_send = Interface.action #a modifier avec Victor
            				else:
            				   	print(f"{message[message.index('$')+1:]}")
        		except:
            			print("[ERREUR] Connexion au serveur perdue.")
            			client_socket.close()
            			break

	def start_client(self):
    		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    		server_ip = self.ip
    		server_port = 5000

    		try:
        		client.connect((server_ip, server_port))
        		print("[CONNECTÉ] Connexion au serveur réussie.")
    		except:
        		print("[ERREUR] Impossible de se connecter au serveur.")
        		return

    		client.send(f"pseudo${self.username}".encode('utf-8'))

    		# Thread pour recevoir des messages
    		thread = threading.Thread(target=self.receive_messages, args=(client,))
    		thread.start()

    		# Envoyer des messages
    		while True:
        		if message.lower() == "quit":
            			client.send(f"{self.username} a quitté le chat.".encode('utf-8'))
            			client.close()
            			break
            		elif self.to_send != None:
        			client.send(str(self.to_send).encode('utf-8'))
        			self.to_send = None

