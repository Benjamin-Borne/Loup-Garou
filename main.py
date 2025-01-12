import argparse
import time
import threading
import client
import CycleReseau
import server

def new_game(nbplayer, port=5000):
	"""
		Fonction permettant de créer une partie.
	"""
	ip = server.get_ip()
	key = server.keygen(ip)
	Game = CycleReseau.GameServer(ip, nbplayer, port)
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

	parser = argparse.ArgumentParser(description = "Bienvenue sur la page d'aide de notre projet.")

	parser.add_argument("--create", action='store_true', help = "Créer une partie")
	parser.add_argument("--join", action='store_true', help = "Rejoint une partie.")
	parser.add_argument("-p", "--port", type=int, help = "Port sur lequel vous souhaitez créer le serveur. (defaut 5000)")
	parser.add_argument("-k", "--key", type=str, help = "Clé de connection à la partie")
	parser.add_argument("-u", "--username", type=str, help = "Nom d'utilisateur de la partie.")
	parser.add_argument("-n", "--number", type=int, help="Nombre de joueur")
	parser.add_argument('-s', "--save", action='store_true', help = "Permet de rejoindre une partie interrompue.")

	args = parser.parse_args()

	if args.create:
		ip = server.get_ip()
		port = 5000
		if args.port:
			port = args.port
			to_keygen = server.keygen(ip+"$"+str(port))
			thread1 = threading.Thread(target = new_game, args=(args.number, args.port,), daemon=True)
		else:
			to_keygen = server.keygen(ip+"$5000")
			thread1 = threading.Thread(target = new_game, args=(args.number,))

		print(to_keygen)

		thread1.start()
		time.sleep(0.3)
		client.MyClient(args.username, ip, port).start_client()
	elif args.join:
		if args.key:
			ip_serveur, port_serveur = server.keygenRev(args.key).split("$")[0], int(server.keygenRev(args.key).split("$")[1])
			client.MyClient(args.username, ip_serveur, port_serveur).start_client()
		else:
			parser.print_usage()
	else:
		parser.print_usage()
