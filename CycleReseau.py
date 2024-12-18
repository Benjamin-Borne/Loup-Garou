import threading
import random
import Role
import Composition
import server
import ast


class Cycle:

    """
    Classe représentant la gestion du cycle jour/nuit.

    Attributs :
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

    def __init__(self, serv, players_number):

        """
        Initialise un cycle de jeu.

        Args:
            serveur (ChatServer) : Socket du serveur.
        """ 
        self.serveur = serv
        while len(self.serveur.getClients()) != players_number:
            time.sleep(0.3)
                
        self.players = self.serveur.getClients() #Socket des joueurs (à ne pas toucher)
        self.pseudo = self.serveur.getPseudo() #Pseudo des joueurs (à ne pas toucher)


        #affectation aléatoire des rôles
        self.role = Composition.createComp(len(self.players))
        for i in range(len(self.role)):
            self.role[i].nom = self.pseudo[i]
            self.serveur.send(f"PlayListe${str(self.pseudo)}${self.role[i].role}".encode('utf-8'), self.players[i])

            self.nuit_numero = 0

            self.jour = False

            self.amoureux = []
            self.votes = []
                
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
        
        
        #Afficher message
        """
        format message:
                        destination$data@typeAction
        """
        
        message = "all$Cupidon choisi les amoureux.".encode('utf-8')
        self.serveur.broadcast(message, "") #Envoie du message à tous les joueurs.
        
        #Cupidon choisis
        cupidon_socket = self.players[self.pseudo.index(cupidon.nom)]
        self.serveur.send("CCUP$Sélectionne deux amoureux.".encode('utf-8'), cupidon_socket)
        response = cupidon_socket.recv(1024).decode('utf-8') #réponse de la forme "['pseudo1', 'pseudo2']" (type str)
        joueur1, joueur2 = ast.litteral_eval(response)[0], ast.litteral_eval(response)[1] #retransformation en liste puis récupération des pseudos
        

        if joueur1 and joueur2 and joueur1 != joueur2:
            self.amoureux = [self.trouver_joueur(joueur1), self.trouver_joueur(joueur2)]
            #Message aux amoureux
            self.serveur.send(f"Tu es amoureux avec {self.amoureux[1].nom}".encode('utf-8'), self.players[self.pseudo.index(self.amoureux[0].nom)])
            self.serveur.send(f"Tu es amoureux avec {self.amoureux[0].nom}".encode('utf-8'), self.players[self.pseudo.index(self.amoureux[1].nom)])
            self.serveur.send("Le couple est formé".encode('utf-8'),cupidon_socket)
        else:
            self.serveur.broadcast("Aucun couple n'a été formé",cupidon_socket)
        
        
    def phase_voleur(self):
        """
            Méthode permmettant de voler une carte
        """
        
        self.serveur.broadcast(message, "")
        for player in self.role:
            if isinstance(player, Role.Voleur) and player.peut_voler:
                voleur = player
        if self.nuit_numero == 1:
            volable = []
            for player in self.role:
                if player.role != "Voleur":
                    volable.append(player)

            self.serveur.broadcast("message", serveur_socket)# pas compris quoi envoyer
            
            voleur_socket = self.players[self.pseudo.index(voleur.nom)]
            self.serveur.send("CVOL$Quelle personne veux tu voler ?".encode('utf-8'),voleur_socket)
            
            response = voleur_socket.recv(1024).decode('utf_8')#pseudo
            
            if response:
                vole = self.trouver_joueur(vole)
                self.serveur.send("Tu as volé: "+vole.role.encode('utf-8'),voleur_socket) #envoie du message au voleur
                self.serveur.send("Tu as été volé".encode('utf-8'), self.players[self.pseudo.index(vole)]) #envoie du message au volé

    def tour_nuit(self):
        """
        Exécute un tour de nuit :
        - Les Loups-Garous choisissent une victime.
        - La Voyante sonde un joueur.
        - La Sorcière agit (potion de vie ou de mort).

        Met à jour les statuts des joueurs en fonction des actions effectuées.
        """
        self.jour = False
        self.serveur.broadcast("Nuit numéro {self.nuit}".encode('utf-8'), "")

        # Les Loups-Garous choisissent une victime
        loups = [j for j in self.role if isinstance(j, Role.LoupGarou) and j.est_vivant]
        loups_socket = [self.players[self.pseudo.index(j.nom)] for j in loups]
        
        villageois = [j for j in self.role if not isinstance(j, Role.LoupGarou) and j.est_vivant]
        villageois_socket = [self.players[self.pseudo.index(j.nom)] for j in villageois]
        
        victime = None

        #A faire ps c comme les votes
        while victime == None:
            for sock in loups_socket:
                self.serveur.send("VLOU$Choisissez ue victime.".encode('utf-8'), sock)
            vote = []
            for sock in loups_socket:
                vote.append(sock.recv(1024).decode('utf-8'))
            if len(self.count_occurence(vote)) == 1:
                victime = self.count_occurence(vote)[0]
            else:
                self.serveur.send("VLOU$Veuillez vous mettre d'accord bande de gros fils de pute que vous êtes!!!!!!".encode('utf-8'), sock)
                
        victime_loup = self.trouver_joueur(victime)
        
        

        # La Voyante sonde un joueur
        for player in self.role:
            if isinstance(player, Role.Voyante):
                voyante = player
                
        voyante_socket = self.players[self.pseudo.index(voyante.nom)]
        
        if voyante:
            self.serveur.broadcast("Au tour de la voyante.".encode('utf-8'), "")
            self.serveur.send("CVOY$Sélectionne la personne dont tu veux voir la carte".encode('utf-8'), voyante_socket)
            vu = voyante_socket.recv(1024).decode('utf-8')
            vu = self.trouver_joueur(vu)
            self.serveur.send(f"CVOYREP$Le role en question est : {vu.role}".encode('utf-8') ,voyante_socket)


        # La Sorcière agit
        for player in self.role:
            if isinstance(player, Role.Sorciere):
                sorciere = player
        
        sorciere_socket = self.players[self.pseudo.index(sorciere.nom)]
        
        if sorciere:
            self.serveur.broadcast("Au tour de la sorciere.".encode('utf-8'), "")

        
        self.serveur.send(f"CSORA${victime_loup} est mort que veux tu faire ?".encode('utf-8'), voyante_socket)
        
        #a modif parce voila quoi
        action = sorciere_socket.recv(1024).decode('utf-8')
        if action == "tuer":
            self.serveur.send("SORT$Qui veux tu tuer ?".encode('utf-8'), sorciere_socket)
            victime = voyante_socket.recv(1024).decode('utf-8')
            victime = self.trouver_joueur(victime)
            victime.mourir()
            
        elif action == "sauver":
            victime_loup.est_vivant  = True         

        self.nuit_numero += 1

    def tour_jour(self):
        self.jour = True
        self.votes = []
        self.serveur.broadcast(f"\n--- Jour {self.nuit} ---\n".encode('utf-8'), "")
        
        for i in range(2):
            if not amoureux[i].est_vivant:
                self.serveur.broadcast(f"{amoureux[i].nom} meurt, donc son amoureux {amoureux[(i+1)%2].nom} se suicide.")
                amoureux[(i+1)%2].mourir()

        self.interface.chronometre(30)
        
        self.serveur.broadcast("VOTE$Veuillez voter s'il vous plait.".encode('utf-8'), "")
        vote = []
        #la faut je réfléchisse demain je suis ko technique
        
        if self.votes:
            cible = self.votes[0]  
            self.chat("Maitre du jeu",f"Les villageois votent pour éliminer {cible.nom}.")
            cible.mourir(self)
        else:
            self.chat("Maitre du jeu","Les villageois votent pour n'éliminer personne")

    def lancer_cycle(self, tours):
        """
        Lance une série de cycles jour/nuit.

        Args:
            tours (int) : Nombre total de cycles à exécuter.
        """

        # Phase Cupidon avant la première nuit

        self.interface.updateList(self.role)
        self.phase_cupidon()
        self.phase_voleur()
        
        winner = False
        
        while not winner:
            # Vérifier s'il reste des Loup-Garous vivants
            loups_restants = any(isinstance(j, Role.LoupGarou) and j.est_vivant for j in self.role)
            # Vérifier s'il reste des Villageois vivants
            villageois_restants = any(not isinstance(j, Role.LoupGarou) and j.est_vivant for j in self.joueurs)
            
            if villageois_restants and loups_restants:
                self.tour_nuit()
                self.tour_jour()
            else:
                if not villageois_restants:
                    winner = "Villageois"
                else:
                    winner = "Loup garou"
                    
                        
        self.serveur.broadcast(f"Les winner sont les {winner}".encode('utf-8'), "")
