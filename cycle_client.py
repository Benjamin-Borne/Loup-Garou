import socket
import client
import server

def create():
	"""
		Fonction permettant de créer une partie.
	"""
	ip = server.get_ip()
	key = server.keygen()
	MySock = server.ChatServer(ip, 5000)
	
	MySock.start()
	


def connec_to_party(key : str, username : str):
	"""
		Fonction permettant de rejoindre une partie.
		inputs:
			key (str): clé de connection au serveur
			username (str): nom d'utilisateur du joueur
	"""
	server_ip = server.keygenRev(key)
	new_client = client.MyClient(username, server_ip)
	
	new_client.start_client()
	
	
	
	

