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
								affected_player = ast.literal_eval(message.split("$")[2])
								act1 = self.app.action(affected_player)
								if act1 != None:
									affected_player.remove(act1)
									act2 = self.app.action(affected_player)
									to_send = [act1, act2]
									print(to_send)
								else:
									to_send = None
								to_send = "CUP$"+str(to_send)
								client_socket.send(to_send.encode('utf-8'))
							elif message.split("$")[0] == "CVOL":
								time.sleep(2) 
								affected_player = ast.literal_eval(message.split("$")[2])
								to_send = "VOL$"+str(self.app.action(affected_player))
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
								affected_player = ast.literal_eval(message.split("$")[2])
								self.app.chat(f"Maître du jeu : {message.split('$')[1]}")
								self.app.canChat = True
								self.app.loupChat = True
								thread = threading.Thread(target=self.receive_messages, args = (client_socket,))
								thread.start()
								self.app.chronometre(20)
								self.app.canChat = False
								self.app.loupChat = False
								to_send = self.app.action(affected_player)
								to_send = "LOU$"+str(to_send)
								client_socket.send(to_send.encode('utf-8'))
							elif message.split("$")[0] == "PF":
								thread = threading.Thread(target = self.app.pfTurn)
								thread.start()
								self.app.chronometre(30)
								self.app.pfEnd()
							elif message.split("$")[0] == "CVOY":
								affected_player = ast.literal_eval(message.split("$")[2])
								to_send = "VOY$"+self.app.action(affected_player)
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
								self.app.chat(message.split("$")[1])
								to_send = str(self.app.action(possible_action))
								if to_send == "None" or to_send == "Sauver la victime":
									to_send = "SOR$"+to_send
									client_socket.send(to_send.encode('utf-8'))
								else:
									affected_player = ast.literal_eval(message.split("$")[3])
									to_send = str(self.app.action(affected_player))
									to_send = "SOR$"+str(to_send)
									client_socket.send(to_send.encode('utf-8'))
							elif message.split("$")[0] == "CHASS":
								affected_player = ast.literal_eval(message.split("$")[2])
								self.app.chat(f"Maitre du jeur : {message.split('$')[1]}")
								to_send = "CHA$"+str(self.app.action(affected_player))
								client_socket.send(to_send.encode('utf-8'))
							elif message.split("$")[0] == "MAIREVOTE":
									affected_player = ast.literal_eval(message.split("$")[2])
									self.app.chat(f"Maître du jeu : {message.split('$')[1]}")
									self.app.canChat = True
									thread = threading.Thread(target=self.receive_messages, args = (client_socket,))
									thread.start()
									self.app.chronometre(20)
									self.app.canChat = False
									to_send = self.app.action(affected_player, True)
									to_send = "VOTE$"+str(to_send)
									print(to_send)
									client_socket.send(to_send.encode('utf-8'))
							elif message.split("$")[0] == "VOTE":
									affected_player = ast.literal_eval(message.split("$")[2])
									affected_player.remove(self.username)
									self.app.chat(f"Maître du jeu : {message.split('$')[1]}")
									self.app.canChat = True
									thread = threading.Thread(target=self.receive_messages, args = (client_socket,))
									thread.start()
									self.app.chronometre(20)
									self.app.canChat = False
									to_send = self.app.action(affected_player)
									to_send = "VOTE$"+str(to_send)
									client_socket.send(to_send.encode('utf-8'))
							elif message.split("$")[0] == "LISTE":
								player_alive = ast.literal_eval(message.split("$")[1])
								self.app.updateList(player_alive)
							elif message.split("$")[0] == "MAIRE":
								affected_player = ast.literal_eval(message.split("$")[2])
								to_send = self.app.action(affected_player)
								to_send = "MAIREP$"+to_send
								client_socket.send(to_send.encode('utf-8'))
							else:
								to_chat = message.split("$")[1]
								try:
									self.app.chat(message.split("$")[2], to_chat)
								except Exception as e:
									print(f"Error : {e}")
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
