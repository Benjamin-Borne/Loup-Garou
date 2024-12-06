import socket
import Interface
import Role
import server
import cycle_client
import CycleReseau


def new_game():
	
	"""
		Fonction permettant de créer une partie.
	"""
	ip = server.get_ip()
	key = server.keygen()
	MySock = server.ChatServer(ip, 5000)
	
	MySock.start()
	

	
def join_game(key: str):
	
	"""
		Fonction permettant de rejoindre une partie.
		inputs:
			key (str): clé de connection au serveur
			username (str): nom d'utilisateur du joueur
	"""
	server_ip = server.keygenRev(key)
	new_client = client.MyClient(username, server_ip)
	
	new_client.start_client()
	
	
def deroulement_party():



	"""
		Fonction du déroulement de la partie. Lancée une fois la partie initialisée.
	"""

	player = NewPlayer(username)
	






	CycleReseau.nuit1()
	
	loups_restants = any(isinstance(j, Role.LoupGarou) and j.est_vivant for j in self.joueurs)
	villageois_restants = any(not isinstance(j, Role.LoupGarou) and j.est_vivant for j in self.joueurs)
	
	while not loups_restant or villageois_restants:+
		nuit()
		jour()
		loups_restants = any(isinstance(j, Role.LoupGarou) and j.est_vivant for j in self.joueurs)
		villageois_restants = any(not isinstance(j, Role.LoupGarou) and j.est_vivant for j in self.joueurs)
	

