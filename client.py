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
                			print(f"\n{message}")
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

