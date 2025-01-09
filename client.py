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
							print(str(message.split("$"))+"\n")
							if message.split("$")[0] == "PlayListe":
								usernames = ast.literal_eval(message.split("$")[1])
								print(usernames)
								self.liste_joueur = usernames
								self.app.after(0, self.app.startUpdates, *(self.liste_joueur, message.split("$")[2]))
								self.app.after(0, self.app.deiconify)
							elif message.split("$")[0] == "CCUP":
								print("ici cupidon")
								act1 = self.app.action(self.liste_joueur)
								if act1 != None:
									act2 = self.app.action(self.liste_joueur)
									to_send = [act1, act2]
								to_send = "CUP$"+str(to_send)
								client_socket.send(to_send.encode('utf-8'))
							elif message.split("$")[0] == "CVOL":
								time.sleep(2) 
								print("En attente d'une action à envoyer au serveur...")
								to_send = "VOL$"+str(self.app.action(self.liste_joueur))
								print(f"Action choisie : {to_send}")
								try:
									client_socket.send(to_send.encode('utf-8'))
								except Exception as e:
									print(f"Erreur lors de l'envoi : {e}")
							elif message.split("$")[0]=="CVOLREP":
								try:
									role = message.split('$')[1].split(':')[1][1:].lower()
									print(role+"\n")
									self.app.changeImage(role)
								except Exception as e:
									print(f"Erreur: {e}")
							elif message.split("$")[0]=="VOLE":
								self.app.changeImage("voleur")
							elif message.split("$")[0] == "VLOU":
								self.app.canChat = True
								def handle_action():
									to_send = self.app.action(self.liste_joueur)
									to_send = "LOU$"+str(to_send)
									try:
										client_socket.send(to_send.encode('utf-8'))
									except Exception as e:
										print(f"Erreur lors de l'envoie : {e}")
								try:
									thread = threading.Thread(target = handle_action)
									thread.start()
								except Exception as e:
									print(f"Erreur : {e}")
							elif message.split("$")[0] == "PF":
								print("ici petite fille")
								self.app.pfTurn()
							elif message.split("$")[0] == "CVOY":
								print("ici voyante")
								to_send = "VOY$"+self.app.action(self.liste_joueur)
								try:
									client_socket.send(to_send.encode('utf-8'))	
								except Exception as e:
									print(f"Erreur lors de l'envoie : {e}")
							elif message.split("$")[0] == "CVOYREP":
								self.app.chat(f"Maitre du jeu: Le Joeur a le Rôle: {message[message.index('$')+1:]}\n")

							elif message.split("$")[0] == "SORC":
								print("ici la sorciere")
								possible_action = []
								if 1 in ast.literal_eval(message.split("$")[2]):
									possible_action.append("Sauver la victime")
								if 2 in ast.literal_eval(message.split("$")[2]):
									possible_action.append("Tuer quelqu'un d'autre")
								to_send = str(self.app.action(possible_action))
								if to_send == "None" or to_send == "Sauver la victime.":
									to_send = "SOR$"+to_send
									client_socket.send(to_send.encode('utf-8'))
								else:
									to_send = str(self.app.action(self.liste_joueur))
									to_send = "SOR$"+str(to_send)
									client_socket.send(to_send.encode('utf-8'))
							elif message.split("$")[0] == "VOTE":
								self.app.canChat = True
								self.app.chronometre(60)
								self.chat = False
								to_send = self.app.action(self.liste_joueur)
								to_send = "VOTE$"+str(to_send)
								client_socket.send(to_send.encode('utf-8'))
							else:
								self.app.chat("Maitre du Jeu\n", message)
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
