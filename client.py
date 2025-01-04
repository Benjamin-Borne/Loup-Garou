import socket
import threading
import Interface
import ast
import Role

class MyClient:

	def __init__(self, username : str, ip : str, port: int):
		self.username = username
		self.ip = ip
		self.port = port
		self.to_send = None
		self.liste_joueur = []
		self.app = None
		self.client = None
		
		
	def receive_messages(self, client_socket):
			while True:
				try:
						message = client_socket.recv(1024).decode('utf-8')
						if message:
							print(message)
							if message.split("$")[0] == "PlayListe":
								print("ici")
								self.app.after()
							elif message.split("$")[0] == "CCUP":
								self.to_send = []
								self.to_send.append(Interface.action(self.liste_joueur))
							elif message.split("$")[0] == "CVOL":
								self.to_send = Interface.action(self.liste_joueur) 
								#changer image
							elif message.split("$")[0] == "VLOU":
								self.to_send = Interface.action([joueur for joueur in self.liste_joueur if not isinstance(joueur, Role.LoupGarou)]) 
							elif message.split("$")[0] == "CVOY":
								self.to_send = Interface.action([joueur for joueur in self.liste_joueur if not isinstance(joueur, Role.Voyante)]) 	
							elif message.split("$")[0] == "CVOY":
								#a voir si vraiment util
								print(f"{message[message.index('$')+1:]}")
							elif message.split("$")[0] == "CORSA":
								print(message.split("$")[1]) #la c'est de la merde
								self.to_send = Interface.action(self.liste_joueur)
							elif message.split("$")[0] == "CSORST":
								self.to_send = Interface.action(['sauver', 'tuer', 'Ne rien Faire'])
							elif message.split("$")[0] == "VOTE":
								self.to_send = Interface.action([joueur for joueur in self.liste_joueur if not joueur.nom != self.username])
							else:
								print(f"{message[message.index('$')+1:]}")
				except:
						print("[ERREUR] Connexion au serveur perdue.")
						client_socket.close()
						break

	def start_client(self):
			self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server_ip = self.ip
			server_port = self.port

			try:
				self.client.connect((server_ip, server_port))
				print("[CONNECTÉ] Connexion au serveur réussie.")
			except:
				print("[ERREUR] Impossible de se connecter au serveur.")
				return

			self.client.send(f"pseudo${self.username}".encode('utf-8'))

			self.app = Interface.mainInterface([], "", self.client)
			# Thread pour recevoir des messages
			thread = threading.Thread(target=self.receive_messages, args=(self.client,), daemon=True)
			thread.start()

			self.app.mainloop()
