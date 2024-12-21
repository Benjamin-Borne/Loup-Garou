import socket
import sys
import time
import threading
import client
import Interface
import CycleReseau
import server
import base64

def new_game():
	"""
		Fonction permettant de créer une partie.
	"""
	ip = server.get_ip()
	key = server.keygen(ip)
	Game = CycleReseau.GameServer(ip, 1, 5000)
	Game.start()

def connect_to_party(key : str, username : str):
	"""
		Fonction permettant de rejoindre une partie.
		inputs:
			key (str): clé de connection au serveur
			username (str): nom d'utilisateur du joueur
	"""
	server_ip = server.keygenRev(key)
	new_client = client.MyClient(username, server_ip)
	
	new_client.start_client()
	

if __name__ == "__main__":
	if sys.argv[1] == "--create":
		ip = server.get_ip()
		thread1 = threading.Thread(target = new_game)
		thread1.start()
		time.sleep(0.3)
		client.MyClient("benji", ip).start_client()
		
	else:
		thread1 = threading.Thread(target=connect_to_party, args = (sys.argv[5], sys.argv[3],))
		thread1.start()
		
