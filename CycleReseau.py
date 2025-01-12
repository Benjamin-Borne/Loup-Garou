from collections import Counter
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
        afficher_joueurs() : Met à jour l'interface avec les joueurs vivants.
        chat(joueur, message) : Ajoute un message au chat.
        vote() : Enregistre un vote contre un joueur.
        phase_cupidon() : Exécute la phase où Cupidon lie des amoureux.
        phase_voleur() : Exécute la phase où le Voleur vole un rôle.
        phase_sorciere() : Exécute la phase de jeu de la sorcière.
        phase_loup() : Exécute le vote des loups
        phase_maire() : Procède au vote pour élire le maire
        phase_chasseur() : Exécute la phase de jeu du chasseur
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
        self.maire = None
        self.sock_maire = None
        

        self.nuit_numero = 0
        self.jour = False
        self.amoureux = []
        self.votes = []
        self.data_client = {}

                
    def trouver_joueur(self, nom : str) -> Role.Joueur:
        """
            Fonction permettant de trouver un joueur
            Input:
                -nom (str) : pseudos du joeur
        """
        for joueur in self.role:
            if joueur.nom == nom:
                return joueur


    def count_occurence(self, L : list) -> list:
        if not L:
            return None  # Gestion de la liste vide
        compteur = Counter(L)  # Compte les occurrences de chaque élément
        max_occurrence = max(compteur.values())  # Trouve le maximum des occurrences
        elements_max = [element for element, count in compteur.items() if count == max_occurrence]
        return elements_max


    def phase_cupidon(self):
        """
            Fonction permettant d'effectuer la création du couple.
        """

        for j in self.role:
            if isinstance(j, Role.Cupidon):
                cupidon = j
        if cupidon.est_vivant:
            message = "CHAT$Cupidon choisi les amoureux.$Maitre du jeu"

            self.broadcast(message, "") #Envoie du message à tous les joueurs.
            
            #Cupidon choisis
            cupidon_socket = self.clients[self.pseudos.index(cupidon.nom)]
            time.sleep(2)

            affected_player = str([player.nom for player in self.role if player.nom != cupidon.nom and player.est_vivant])

            self.send_msg(f"CCUP$Sélectionne deux amoureux.${affected_player}".encode('utf-8'), cupidon_socket)

            while not self.data_client[cupidon_socket]:
                time.sleep(0.1)
            
            response = self.data_client[cupidon_socket]
            
            if response == "None":
                self.amoureux = None
                self.broadcast("CHAT$Aucun couple n'a été formé.$Maitre du jeu", "")
            else:
                self.amoureux = [self.trouver_joueur(response[0]), self.trouver_joueur(response[1])]
                amoureux1_socket, amoureux2_socket = self.clients[self.pseudos.index(self.amoureux[0].nom)], self.clients[self.pseudos.index(self.amoureux[1].nom)]
                self.send_msg(f"CHAT$Tu est amoureux avec : {self.amoureux[1].nom}$Maitre du jeu".encode('utf-8'), amoureux1_socket)
                self.send_msg(f"CHAT$Tu est amoureux avec : {self.amoureux[0].nom}$Maitre du jeu".encode('utf-8'), amoureux2_socket)  
                self.broadcast("CHAT$Le couple a été formé.$Maitre du jeu", "") 

            self.data_client[cupidon_socket] = False

    def phase_voleur(self):
        """
            Méthode permmettant de voler une carte
        """
        for player in self.role:
            if isinstance(player, Role.Voleur):
                voleur = player
        if voleur.est_vivant:
            self.broadcast("CHAT$Le voleur se réveil.$Maitre du jeu", "")
            
            if self.nuit_numero == 0:
                volable = []
                for player in self.role:
                    if player.role != "Voleur":
                        volable.append(player)
                
                voleur_socket = self.clients[self.pseudos.index(voleur.nom)]

                affected_player = str([player.nom for player in self.role if player.nom != voleur.nom and player.est_vivant])

                time.sleep(2)
                self.send_msg(f"CVOL$Quelle personne veux tu voler ?${affected_player}".encode('utf-8'),voleur_socket)
                while not self.data_client[voleur_socket]: #attente de la réponse du voleur
                    time.sleep(0.1)
                response = self.data_client[voleur_socket]
                if response:
                    if response == 'None':
                        self.send_msg("CHAT$Tu n'as volé aucun rôle.$Maitre du jeu".encode('utf-8'), voleur_socket)
                    else:
                        vole = self.trouver_joueur(response) 
                        to_send = "CVOLREP$Tu as volé: "+vole.role
                        self.send_msg(to_send.encode('utf-8'),voleur_socket) #envoie du message au voleur
                        self.send_msg("VOLE$Tu as été volé".encode('utf-8'), self.clients[self.pseudos.index(vole.nom)]) #envoie du message au volé

                        vole.nom, voleur.nom = voleur.nom, vole.nom

                self.data_client[voleur_socket] = False

    def phase_voyante(self):
        #Recherche de la voyante
        for player in self.role:
            if isinstance(player, Role.Voyante):
                voyante = player

        if voyante.est_vivant:        
            voyante_socket = self.clients[self.pseudos.index(voyante.nom)]
            affected_player = str([player.nom for player in self.role if player.nom != voyante.nom and player.est_vivant])
            if voyante:
                time.sleep(0.5)
                self.broadcast("CHAT$Au tour de la voyante.$Maitre du jeu", "")
                time.sleep(0.5)
                self.send_msg(f"CVOY$Sélectionne la personne dont tu veux voir la carte${affected_player}".encode('utf-8'), voyante_socket)

                while not self.data_client[voyante_socket]:
                    time.sleep(0.1)

                response = self.data_client[voyante_socket]
                if response != None:
                    to_send = self.trouver_joueur(response).__class__.__name__
                    to_send = "CVOYREP$"+to_send+"$"+self.data_client[voyante_socket]
                    self.send_msg(to_send.encode('utf-8'), voyante_socket)
                self.data_client[voyante_socket] = False

    def phase_loups(self):
        
        time.sleep(1)
        # Création de la liste des sockets des loups
        loups = [j for j in self.role if isinstance(j, Role.LoupGarou) and j.est_vivant]
        loups_socket = [self.clients[self.pseudos.index(j.nom)] for j in loups]

        if self.nbPlayers in [10,12,14,16,17,18]:
            for pf in self.role:
                if isinstance(pf, Role.PetiteFille):
                    petite_fille = pf
        victime = None
        affected_player = str([player.nom for player in self.role if player not in loups and player.est_vivant])
        while victime == None:
            for sock in loups_socket:
                self.send_msg(f"VLOU$Choisissez ue victime.${affected_player}".encode('utf-8'), sock)
            if self.nbPlayers in [10,12,14,16,17,18]:
                time.sleep(0.5)
                if petite_fille.est_vivant:
                    self.send_msg("PF$Le tour des loups a commencé".encode('utf-8'), self.clients[self.pseudos.index(petite_fille.nom)])

            while not all([self.data_client[el] for el in self.data_client.keys() if el in loups_socket]):
                time.sleep(0.1)
            
            vote = [self.data_client[el] for el in self.data_client.keys() if el in loups_socket]
            vote = self.count_occurence(vote)

            if len(vote) == 1:
                victime = vote[0]
                victime = self.trouver_joueur(victime)
                for sock in loups_socket:
                    self.data_client[sock] = False
                if 'petite_fille' in locals():
                    self.data_client[self.clients[self.pseudos.index(petite_fille.nom)]] = False
                return victime
            else:
                for sock in loups_socket:
                    self.data_client[sock] = False
                    self.send_msg("CHAT$Veuillez vous mettre d'accord s'il vous plaît$Maitre du jeu".encode('utf-8'), sock)
                if 'petite_fille' in locals():
                    self.data_client[self.clients[self.pseudos.index(petite_fille.nom)]] = False    
                time.sleep(0.5)
                self.phase_loups()
            
    def phase_sorciere(self, victime):
        time.sleep(1)
        for player in self.role:
            if isinstance(player, Role.Sorciere):
                sorciere = player
        if sorciere.est_vivant and (sorciere.potion_mort or sorciere.potion_vie):
            self.broadcast("CHAT$Au tour de la sorcière.\n$Maitre du jeu", "")
            sorciere_socket = self.clients[self.pseudos.index(sorciere.nom)]
            affected_player = str([player.nom for player in self.role if player.nom != sorciere.nom and player.est_vivant])
            possible_action = []
            if sorciere.potion_vie:
                possible_action.append(1)
            if sorciere.potion_mort:
                possible_action.append(2)
            time.sleep(0.5)
            self.send_msg(f"SORC${victime.nom} est mort, que veux tu faire ?${str(possible_action)}${affected_player}".encode('utf-8'), sorciere_socket)

            while not self.data_client[sorciere_socket]:
                time.sleep(0.1)

            response = self.data_client[sorciere_socket]

            if response == "Sauver la victime":
                sorciere.potion_vie = False
                victime.est_vivant = True
                self.data_client[sorciere_socket] = False
                return "sauver"
            elif response == "None":
                self.data_client[sorciere_socket] = False
                return None
            else:
                sorciere.potion_mort = False
                victime_sor = self.trouver_joueur(response)
                self.data_client[sorciere_socket] = False
                return victime_sor

    def phase_chasseur(self):
        self.broadcast("CHAT$Cette personne est le chasseur.$Maitre du jeu", "")
        time.sleep(0.3)
        for player in self.role:
            if isinstance(player, Role.Chasseur):
                chasseur = player
        
        chasseur_socket = self.clients[self.pseudos.index(chasseur.nom)]
        affected_player = str([player.nom for player in self.role if player.nom != chasseur.nom and player.est_vivant])
        self.send_msg(f"CHASS$Qui veux tu entrainer dans ta mort ?${affected_player}".encode('utf-8'), chasseur_socket)

        while not self.data_client[chasseur_socket]:
            time.sleep(0.1)

        if self.data_client[chasseur_socket] != "None":
            self.trouver_joueur(self.data_client[chasseur_socket]).est_vivant = False
            victime = self.data_client[chasseur_socket]
            self.data_client[chasseur_socket] = False
            return victime
        self.data_client[chasseur_socket] = False
        return None
    
    def phase_maire(self):

        while not all([self.data_client[sock] for sock in self.clients]):
            time.sleep(0.1)
        vote = self.count_occurence([self.data_client[sock] for sock in self.clients])
        if len(vote) != 1:
            for sock in self.clients:
                self.data_client[sock] = False
            self.broadcast(f"VOTE$Veuillez vous décider s'il vous plaît.${self.pseudos}", "")
            self.phase_maire()
        else:
            for sock in self.clients:
                self.data_client[sock] = False
            return vote[0]

    def tour_nuit(self):
        """
        Exécute un tour de nuit :
        - Les Loups-Garous choisissent une victime.
        - La Voyante sonde un joueur.
        - La Sorcière agit (potion de vie ou de mort).

        Met à jour les statuts des joueurs en fonction des actions effectuées.
        """
        self.jour = False
        self.broadcast(f"CHAT$\n-------------------\nNuit numéro {self.nuit_numero}\n$", "")

        self.phase_voyante()
        time.sleep(1)
        self.broadcast("CHAT$Les loups se réveillent$Maitre du jeu", "")
        victime_loups = self.phase_loups()
        time.sleep(1)
        if self.nbPlayers in [11,13,15,16,17,18]:
            witch_action = self.phase_sorciere(victime_loups)       

            if witch_action == None:
                victimes = [victime_loups]
            elif witch_action == "sauver":
                self.nuit_numero+=1
                return []
            else:
                victimes = [victime_loups, witch_action]
            self.nuit_numero += 1
        else:
            victimes = [victime_loups]

        self.nuit_numero+=1
        return victimes

    def tour_jour(self, victimes):
        def find_lover():
            mort = False
            if self.amoureux != None:
                for i in range(2):
                    if not self.amoureux[i].est_vivant:
                        mort = True
                        self.amoureux[(i+1)%2].mourir()
                if mort:
                    self.broadcast(f"CHAT${self.amoureux[0].nom} meurt, donc son amoureux {self.amoureux[1].nom} se suicide.$Maitre du jeu", "")
                    

        self.jour = True
        self.votes = []

        for vic in victimes:
            vic.est_vivant = False

        time.sleep(0.3)
        if len(victimes) == 2:
            victimes_sock = [self.clients[self.pseudos.index(victimes[0].nom)], self.clients[self.pseudos.index(victimes[1].nom)]]
            self.broadcast(f"CHAT$Ces personnes sont mortes cette nuit: {victimes[0].nom, victimes[1].nom}$Maitre du jeu", "")
            time.sleep(1)
        elif len(victimes) == 1:
            victimes_sock = [self.clients[self.pseudos.index(victimes[0].nom)]]
            self.broadcast(f"CHAT$Cette personne est morte cette nuit: {victimes[0].nom}$Maitre du jeu", "")
            time.sleep(1)
        else:
            victimes_sock = ()
            self.broadcast("CHAT$Aucune personne n'est morte cette nuit.$Maitre du jeu", "")
            time.sleep(1)
        
        for el in victimes:
            if el.role == "Chasseur":
                self.phase_chasseur()
            if el.nom == self.maire.nom:
                affected_player = [player.nom for player in self.role if player.est_vivant]
                self.send_msg(f"MAIRE$Tu dois sélectionner le future maire${affected_player}".encode('utf-8'), self.sock_maire)
                while not self.data_client[self.sock_maire]:
                    time.sleep(0.1)
                self.maire = self.trouver_joueur(self.data_client[self.sock_maire])
                self.data_client[self.sock_maire] = False
                self.sock_maire = self.clients[self.pseudos.index(self.maire.nom)]
                time.sleep(0.5)
                self.broadcast(f"CHAT$Le nouveau maire est : {self.maire.nom}$Maitre du jeu", "")

        find_lover()
        affected_player = [player.nom for player in self.role if player.est_vivant]
        
        time.sleep(0.3)
        for player in self.role:
            if player.est_vivant:
                self.send_msg(f"VOTE$Vous avez une minute pour choisir qui éliminer${affected_player}".encode('utf-8'), self.clients[self.pseudos.index(player.nom)])
            else:
                self.send_msg(f"CHAT$Vous avez une minute pour choisir qui éliminer$Maitre du jeu".encode('utf-8'), self.clients[self.pseudos.index(player.nom)])

        while not all([self.data_client[self.clients[self.pseudos.index(player.nom)]] for player in self.role if player.est_vivant]):
            time.sleep(0.1)

        vote = self.count_occurence([self.data_client[sock] for sock in self.data_client.keys()])  
        if vote == "None":
            self.broadcast("CHAT$Personne n'a été désigné.$Maitre du jeu", "")
            return
        elif len(vote) > 1:
            vote = self.count_occurence([self.data_client[sock] for sock in self.data_client.keys()]+[self.data_client[self.sock_maire]])
        
        print(vote)
        vote = self.trouver_joueur(vote[0])
        vote.est_vivant = False

        self.broadcast(f"CHAT${vote.nom} a été éliminé. {vote.nom} était {vote.role}$Maitre du jeu", "")

        find_lover()

        for sock in self.data_client.keys():
            self.data_client[sock] = False

        if vote.role == "Chasseur":
            victime = self.phase_chasseur()
            if victime == None:
                self.broadcast("CHAT$Le chasseur a décidé de mourir seul$Maitre du jeu", "")
            else:
                self.broadcast(f"CHAT$Le chasseur entraine {victime} dans sa mort.$Maitre du jeu", "")
                victime = self.trouver_joueur(victime)
                victime.est_vivant = False
            
            

    def lancer_cycle(self):
        """
        Lance une série de cycles jour/nuit.

        Args:
            tours (int) : Nombre total de cycles à exécuter.
        """

        if self.nuit_numero == 0:
            self.broadcast(f"MAIREVOTE$Vous devez élire un maire.${self.pseudos}", "")
            time.sleep(0.2)
            self.maire = self.trouver_joueur(self.phase_maire())
            time.sleep(0.5)
            self.broadcast(f"CHAT$Le maire est : {self.maire.nom}$Maitre du jeu.", "")
            self.sock_maire = self.clients[self.pseudos.index(self.maire.nom)]
            time.sleep(0.5)
            if self.nbPlayers in [12,13,14,15,16,17,18]:
                self.phase_voleur()
            if self.nbPlayers in [8, 9,10,11,12,13,14,15,16,17,18]:
                self.phase_cupidon()
                time.sleep(0.2)

        self.nuit_numero+=1

        winner = False
        
        while not winner:
            # Vérifier s'il reste des Loup-Garous vivants
            loups_restants = any(isinstance(j, Role.LoupGarou) and j.est_vivant for j in self.role)
            # Vérifier s'il reste des Villageois vivants
            villageois_restants = any(not isinstance(j, Role.LoupGarou) and j.est_vivant for j in self.role)
            
            if villageois_restants and loups_restants :
                victimes = self.tour_nuit()
                time.sleep(1)
                self.broadcast(f"CHAT$\n--- Jour {self.nuit_numero-1} ---\n$", "")
                self.tour_jour(victimes)
                time.sleep(0.2)
                player_alive = [player.nom for player in self.role if player.est_vivant]
                self.broadcast(f"LISTE${player_alive}", "")
                time.sleep(0.5)
                if not self.maire.est_vivant:
                    affected_player = [player.nom for player in self.role if player.est_vivant]
                    self.send_msg(f"MAIRE$Tu dois sélectionner le future maire${affected_player}".encode('utf-8'), self.sock_maire)
                    while not self.data_client[self.sock_maire]:
                        time.sleep(0.1)
                    self.maire = self.trouver_joueur(self.data_client[self.sock_maire])
                    self.data_client[self.sock_maire] = False
                    self.sock_maire = self.clients[self.pseudos.index(self.maire.nom)]  

                alive_player = [player for player in self.role if player.est_vivant]
                if len(alive_player) == 2:
                    if all(item in self.amoureux for item in alive_player):
                        winner = "Les amoureux ont gagnés."
            else:
                if not villageois_restants:
                    winner = "Loup garou"
                else:
                    winner = "Villageois"
                    
                        
        self.broadcast(f"CHAT$Les winner sont les {winner}$Maitre du jeu", "")
        
    def handle_client(self, client_socket, address):
        print(f"[NOUVEAU CLIENT] {address} connecté.")
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                
                if message:
                    if message.split("$")[0] == "pseudo":
                        self.pseudos.append(message.split("$")[1])
                        self.data_client[client_socket] = False
                    elif message.split("$")[0] == "CHAT":
                        try:
                            to_send = message+"$"+self.pseudos[self.clients.index(client_socket)]
                            self.broadcast(to_send, "")
                        except Exception as e:
                            print(f"Erreur lors de l'envoie : {e}")
                    elif message.split("$")[0] == "VOL":
                        self.data_client[client_socket] = message.split("$")[1]
                        print(self.data_client[client_socket])
                    elif message.split("$")[0] == "CUP":
                        if message.split("$")[1] == "None":
                            self.data_client[client_socket] = "None"
                        else:
                            self.data_client[client_socket] = ast.literal_eval(message.split("$")[1])
                    elif message.split("$")[0] == "VOY":
                        self.data_client[client_socket] = message.split("$")[1]
                    elif message.split("$")[0] == "LOU":
                        self.data_client[client_socket] = message.split('$')[1]
                    elif message.split("$")[0] == "LOUM":
                        if self.nbPlayers in [10,12,14,16,17,18]:
                            for pf in self.role:
                                if isinstance(pf, Role.PetiteFille):
                                    petite_fille = pf
                            pf_sock = self.clients[self.pseudos.index(petite_fille.nom)]
                        loups = [j for j in self.role if isinstance(j, Role.LoupGarou) and j.est_vivant]
                        loups_sock = [self.clients[self.pseudos.index(j.nom)] for j in loups]
                        to_send = "CHAT$"+message.split("$")[1]+"$"+self.pseudos[self.clients.index(client_socket)]
                        for sock in loups_sock:
                            sock.send(to_send.encode("utf-8"))
                        if 'pf_sock' in locals():
                            to_send = "PFLOU$"+message.split("$")[1]+"$"+self.pseudos[self.clients.index(client_socket)]
                            pf_sock.send(to_send.encode('utf-8'))
                    elif message.split("$")[0] == "PFEND":
                        to_send = f"CHAT${self.pseudos[self.clients.index(client_socket)]} est la petite fille.$Maitre du jeu"
                        self.broadcast(to_send, "")
                    elif message.split("$")[0] == "SOR":
                        self.data_client[client_socket] = message.split("$")[1]
                    elif message.split("$")[0] == "VOTE":
                        self.data_client[client_socket] = message.split("$")[1]
                    elif message.split("$")[0] == "CHA":
                        self.data_client[client_socket] = message.split("$")[1]
                    elif message.split("$")[0] == "MAIREP":
                        self.data_client[client_socket] = message.split("$")[1]
            except:
                break
        print(f"[DÉCONNECTÉ] {address} a quitté.")
        self.clients.remove(client_socket)
        client_socket.close()
    
    def send_msg(self, message, destination):
        destination.send(message)

    def broadcast(self, message, sender_socket):
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
        
