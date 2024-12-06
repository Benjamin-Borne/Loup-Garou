import socket
import Interface
import Role
import server
import cycle_client
import CycleReseau


def new_game():
	
	MyIP = server.get_ip()
	port = 5000
	key = server.keyGen(MyIP)
	
	my_socket = server.MySocket()
	my_socket.start_server()
	

	
def join_game(key: str):
	
	ServerIp = server.decode_keygen(key)
	port = 5000
	
	cycle_client.start_client()
	
	
def deroulement_party():

	player = NewPlayer(username)
	






	CycleReseau.nuit1()
	
	loups_restants = any(isinstance(j, Role.LoupGarou) and j.est_vivant for j in self.joueurs)
	villageois_restants = any(not isinstance(j, Role.LoupGarou) and j.est_vivant for j in self.joueurs)
	
	while not loups_restant or villageois_restants:+
		nuit()
		jour()
		loups_restants = any(isinstance(j, Role.LoupGarou) and j.est_vivant for j in self.joueurs)
		villageois_restants = any(not isinstance(j, Role.LoupGarou) and j.est_vivant for j in self.joueurs)
	

