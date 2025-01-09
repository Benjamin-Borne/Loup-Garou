import socket
import threading
import Interface
import ast
import tkinter
import time
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
								usernames = ast.literal_eval(message.split("$")[1])
								print(usernames)
								self.liste_joueur = usernames
								print("111")
								self.app.after(0, self.app.startUpdates, *(self.liste_joueur, message.split("$")[2]))
								print("222")
								self.app.after(0, self.app.deiconify)
								print("333")
							elif message.split("$")[0] == "CCUP":
								print("ici cupidon")
								act1 = self.app.action(self.liste_joueur)
								if act1 == None:
									client_socket.send("None".encode('utf-8'))
								else:
									act2 = self.app.action(self.liste_joueur)
									client_socket.send(f"[{act1},{act2}]".encode('utf-8'))
							elif message.split("$")[0] == "CVOL":
								time.sleep(2) 
								print("En attente d'une action à envoyer au serveur...")
								to_send = "VOL$"+str(self.app.action(self.liste_joueur))
								print(f"Action choisie : {to_send}")
								try:
									client_socket.send(to_send.encode('utf-8'))
									print("Message envoyé au serveur.")
								except Exception as e:
									print(f"Erreur lors de l'envoi : {e}")
							elif message.split("$")[0]=="CVOLREP":
								role = message.split('$')[1].split(':')[1][1:].lower()
								print(role)
								self.app.changeImage(role)
							elif message.split("$")[0]=="VOLE":
								self.app.changeImage("voleur")
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
								self.app.chat("Maitre du Jeu", message)
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
			
			self.app = Interface.mainInterface([], "simple-villageois", self.client)
			# Thread pour recevoir des messages
			thread = threading.Thread(target=self.receive_messages, args=(self.client,), daemon=True)
			thread.start()

			self.app.mainloop()
