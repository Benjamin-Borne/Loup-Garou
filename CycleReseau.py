import threading
import Role
import Composition
import ast
import time
import socket


class GameServer:

    """
    Classe représentant la gestion du cycle jour/nuit.

    Attributs :
    	host(str) : addresse ip du serveur 
    	port(int) : port de connection du serveur
        joueurs (list) : Liste des joueurs participant à la partie.
        nuit_numero (int) : Compteur de tours de nuit.
        amoureux (list) : Liste des joueurs amoureux.
        jour (bool) : Indique si c'est la phase de jour.
        votes (list) : Liste des votes effectués.

    Méthodes :
        trouver_joueur(nom) : Trouve un joueur par son nom.
        playerAlive() : Retourne la liste des joueurs vivants.
        afficher_joueurs() : Met à jour l'interface avec les joueurs vivants.
        chat(joueur, message) : Ajoute un message au chat.
        vote() : Enregistre un vote contre un joueur.
        phase_cupidon() : Exécute la phase où Cupidon lie des amoureux.
        phase_voleur() : Exécute la phase où le Voleur vole un rôle.
        tour_nuit() : Exécute un tour de nuit avec toutes les actions associées.
        tour_jour() : Exécute un tour de jour avec toutes les actions associées.
        lancer_cycle(tours) : Lance une série de tours jour/nuit.
    """

    def __init__(self, host, players_number, port = 5000):
    	
    	#initialisation du serveur
        self.host = host
        self.port = port
        self.clients = [] #liste des sockets clients
        self.serveur = None    	        

	    #Initialisation du jeu
        self.pseudos = [] #listes de pseudos
        self.nbPlayers = players_number
        self.role = Composition.createComp(self.nbPlayers)

        self.nuit_numero = 0
        self.jour = False
        self.amoureux = []
        self.votes = []
        self.data_client = {}

                
    def trouver_joueur(self, nom : str) -> Role.Joueur:
        for joueur in self.role:
            if joueur.nom == nom:
                return joueur

    def playerAlive(self):
        return [joueur for joueur in self.role if joueur.est_vivant]


    def count_occurence(self, L : list) -> list:
        d = {}
        l_ret = []
        for el in L:
            if el in d.keys():
                d[el]+=1
            else:
                d[el] = 1
        maxi = 0
        for key in d.keys():
            if d[key] > maxi:
                l_ret.append(key)
                maxi = d[key]
            elif d[key] == maxi:
                l_ret.append(key)
        return l_ret


    def nuit1(self):
        
        self.phase_cupidon()
        self.phase_voleur()


    def phase_cupidon(self):
        """
            Fonction permettant d'effectuer la création du couple.
        """

        for j in self.role:
            if isinstance(j, Role.Cupidon):
                cupidon = j
        message = "Cupidon choisi les amoureux."

        self.broadcast(message, "") #Envoie du message à tous les joueurs.
        
        #Cupidon choisis
        cupidon_socket = self.clients[self.pseudos.index(cupidon.nom)]
        time.sleep(2)

        self.send_msg("CCUP$Sélectionne deux amoureux.".encode('utf-8'), cupidon_socket)
        while not self.data_client[cupidon_socket]:
            time.sleep(0.1)
        
        response = self.data_client[cupidon_socket]
        
        if response == None:
            self.broadcast("Aucun couple n'a été formé.", "")
        else:
            self.amoureux = response
            amoureux1_socket, amoureux2_socket = self.clients[self.pseudos.index(self.amoureux[0])], self.clients[self.pseudos.index(self.amoureux[1])]
            self.send_msg(f"Tu est amoureux avec : {self.amoureux[1]}".encode('utf-8'), amoureux1_socket)
            self.send_msg(f"Tu est amoureux avec : {self.amoureux[0]}".encode('utf-8'), amoureux2_socket)  
            self.broadcast("Le couple a été formé.", "") 

        self.data_client[cupidon_socket] = None

    def phase_voleur(self):
        """
            Méthode permmettant de voler une carte
        """
        
        self.broadcast("Le voleur se réveil", "")
        for player in self.role:
            if isinstance(player, Role.Voleur):
                voleur = player
        if self.nuit_numero == 0:
            volable = []
            for player in self.role:
                if player.role != "Voleur":
                    volable.append(player)
            
            voleur_socket = self.clients[self.pseudos.index(voleur.nom)]

            time.sleep(2)
            self.send_msg("CVOL$Quelle personne veux tu voler ?".encode('utf-8'),voleur_socket)
            while not self.data_client[voleur_socket]:
                time.sleep(0.1)
            response = self.data_client[voleur_socket]
            print("response: "+response)
            if response:
                if response == 'None':
                    self.send_msg("Tu n'as volé aucun rôle".encode('utf-8'), voleur_socket)
                else:
                    vole = self.trouver_joueur(response)
                    print([joueur.nom for joueur in self.role])
                    print("Vole : "+vole.__class__.__name__) 
                    to_send = "CVOLREP$Tu as volé: "+vole.role
                    self.send_msg(to_send.encode('utf-8'),voleur_socket) #envoie du message au voleur
                    self.send_msg("VOLE$Tu as été volé".encode('utf-8'), self.clients[self.pseudos.index(vole.nom)]) #envoie du message au volé

                    vole.nom, voleur.nom = voleur.nom, vole.nom
            else:
                print("bouba")
                self.broadcast("Faut choisir.")
            self.data_client[voleur_socket] = None

    def phase_voyante(self):
        # La Voyante sonde un joueur
        for player in self.role:
            if isinstance(player, Role.Voyante):
                voyante = player

        print(voyante.nom)
                
        voyante_socket = self.clients[self.pseudos.index(voyante.nom)]
        
        if voyante:
            self.broadcast("Au tour de la voyante.", "")
            time.sleep(0.5)
            self.send_msg("CVOY$Sélectionne la personne dont tu veux voir la carte".encode('utf-8'), voyante_socket)

            while not self.data_client[voyante_socket]:
                time.sleep(0.1)

            response = self.data_client[voyante_socket]
            print(response)
            if response != None:
                to_send = self.trouver_joueur(response).__class__.__name__
                to_send = "CVOYREP$"+to_send
                self.send_msg(to_send.encode('utf-8'), voyante_socket)
            self.data_client[voyante_socket] = False
    def tour_nuit(self):
        """
        Exécute un tour de nuit :
        - Les Loups-Garous choisissent une victime.
        - La Voyante sonde un joueur.
        - La Sorcière agit (potion de vie ou de mort).

        Met à jour les statuts des joueurs en fonction des actions effectuées.
        """
        self.jour = False
        self.broadcast(f"-------------------\nNuit numéro {self.nuit_numero}", "")

        self.phase_voyante()

        # Les Loups-Garous choisissent une victime
        loups = [j for j in self.role if isinstance(j, Role.LoupGarou) and j.est_vivant]
        loups_socket = [self.clients[self.pseudos.index(j.nom)] for j in loups]
        
        villageois = [j for j in self.role if not isinstance(j, Role.LoupGarou) and j.est_vivant]
        villageois_socket = [self.clients[self.pseudos.index(j.nom)] for j in villageois]
        
        victime = None

        

        #A faire ps c comme les votes
        while victime == None:
            for sock in loups_socket:
                self.send_msg("VLOU$Choisissez ue victime.".encode('utf-8'), sock)
            vote = []
            for sock in loups_socket:
                vote.append(sock.recv(1024).decode('utf-8'))
            if len(self.count_occurence(vote)) == 1:
                victime = self.count_occurence(vote)[0]
            else:
                self.send_msg("VLOU$Veuillez vous mettre d'accord bande de gros fils de pute que vous êtes!!!!!!".encode('utf-8'), sock)
                
        victime_loup = self.trouver_joueur(victime)

        # La Sorcière agit
        for player in self.role:
            if isinstance(player, Role.Sorciere):
                sorciere = player
        
        sorciere_socket = self.clients[self.pseudos.index(sorciere.nom)]
        
        if sorciere:
            self.broadcast("Au tour de la sorciere.", "")

        
        self.send_msg(f"CSORA${victime_loup} est mort que veux tu faire ?".encode('utf-8'), sorciere_socket)
        
        #a modif parce voila quoi
        action = sorciere_socket.recv(1024).decode('utf-8')
        if action == "tuer":
            self.send_msg("SORT$Qui veux tu tuer ?".encode('utf-8'), sorciere_socket)
            victime = sorciere_socket.recv(1024).decode('utf-8')
            victime = self.trouver_joueur(victime)
            victime.mourir()
            
        elif action == "sauver":
            victime_loup.est_vivant  = True         

        self.nuit_numero += 1

    def tour_jour(self):
        self.jour = True
        self.votes = []
        self.broadcast(f"\n--- Jour {self.nuit} ---\n", "")
        
        for i in range(2):
            if not self.amoureux[i].est_vivant:
                self.broadcast(f"{self.amoureux[i].nom} meurt, donc son amoureux {self.amoureux[(i+1)%2].nom} se suicide.", "")
                self.amoureux[(i+1)%2].mourir()

        self.interface.chronometre(30)
        
        self.broadcast("VOTE$Veuillez voter s'il vous plait.", "")
        vote = []
        #la faut je réfléchisse demain je suis ko technique
        
        if self.votes:
            cible = self.votes[0]  
            self.chat("Maitre du jeu",f"Les villageois votent pour éliminer {cible.nom}.")
            cible.mourir(self)
        else:
            self.chat("Maitre du jeu","Les villageois votent pour n'éliminer personne")

    def lancer_cycle(self):
        """
        Lance une série de cycles jour/nuit.

        Args:
            tours (int) : Nombre total de cycles à exécuter.
        """

        # Phase Cupidon avant la première nuit


        self.phase_voleur()
        self.phase_cupidon()

        self.nuit_numero+=1

        winner = False
        
        while not winner:
            # Vérifier s'il reste des Loup-Garous vivants
            loups_restants = any(isinstance(j, Role.LoupGarou) and j.est_vivant for j in self.role)
            # Vérifier s'il reste des Villageois vivants
            villageois_restants = any(not isinstance(j, Role.LoupGarou) and j.est_vivant for j in self.role)
            
            if villageois_restants and loups_restants:
                self.tour_nuit()
                self.tour_jour()
            else:
                if not villageois_restants:
                    winner = "Villageois"
                else:
                    winner = "Loup garou"
                    
                        
        self.broadcast(f"Les winner sont les {winner}", "")
        
    def handle_client(self, client_socket, address):
        print(f"[NOUVEAU CLIENT] {address} connecté.")
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                
                if message:
                    if message.split("$")[0] == "pseudo":
                        self.pseudos.append(message.split("$")[1])
                        self.data_client[client_socket] = False
                        print(self.pseudos)
                    elif message.split("$")[0] == "VOL":
                        print("boobs")
                        self.data_client[client_socket] = message.split("$")[1]
                        print(self.data_client[client_socket])
                    elif message.split("$")[0] == "CUP":
                        print("boobs2")
                        self.data_client[client_socket] = ast.literal_eval(message.split("$")[1])
                    elif message.split("$")[0] == "VOY":
                        print("boobs3")
                        self.data_client[client_socket] = message.split("$")[1]
            except:
                break
        print(f"[DÉCONNECTÉ] {address} a quitté.")
        self.clients.remove(client_socket)
        client_socket.close()
    
    def send_msg(self, message, destination):
        destination.send(message)

    def broadcast(self, message, sender_socket):
        print("debug")
        for client in self.clients:
            client.send(message.encode('utf-8')) 

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(18)
        print(f"[DÉMARRÉ] Serveur en attente de connexions sur {self.host}:{self.port}...")
        
        while len(self.clients) != self.nbPlayers:
            client_socket, client_address = self.server.accept()
            self.clients.append(client_socket)
            thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address), daemon=True)
            thread.start()  

        time.sleep(1)

        #association de joueur selon le nombre de joueur
        for i in range(len(self.pseudos)):
            self.send_msg(f"PlayListe${str(self.pseudos)}${self.role[i].role}".encode('utf-8'), self.clients[i])
            self.role[i].nom = self.pseudos[i]
        time.sleep(1)

        self.lancer_cycle() 
        
