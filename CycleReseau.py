import Interface
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
    
    def __init__(self):
    
        """
        Initialise un cycle de jeu.

        Args:
            joueurs (list) : Liste des joueurs participant à la partie.
        """ 
        self.serveur = server.ChatServer()
        self.players = self.serveure.getClients() #Socket des joueurs (à ne pas toucher)
        self.pseudo = self.serveur.getPseudo() #Pseudo des joueurs (à ne pas toucher)
	
	
	#affectation aléatoire des rôles
	self.role = Composition.createComp(len(self.players))
	for i in range(len(self.role)):
	    self.role[i].nom = self.pseudo[i]
	    		

        self.nuit_numero = 0

        self.jour = False

        self.amoureux = []
        self.votes = []
    	   
    def trouver_joueur(self, nom : str) -> Joueur:
        for joueur in self.role:
            if joueur.nom == nom:
                return joueur

    def playerAlive(self):
        return [joueur for joueur in self.role if joueur.est_vivant]
    
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
            self.serveur.send(f"Tu es amoureux avec {self.amoureux[1].nom}".encode('utf-8'), self.players[self.pseudo.index(self.amoureux[0].nom)
            self.serveur.send(f"Tu es amoureux avec {self.amoureux[0].nom}".encode('utf-8'), self.players[self.pseudo.index(self.amoureux[1].nom)
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

            Reseau.serveur.broadcast("message", serveur_socket)# pas compris quoi envoyer
            
            voleur_socket = self.players[self.pseudo.index(voleur.nom)]
            Reseau.serveur.send("CVOL$Quelle personne veux tu voler ?".encode('utf-8'),voleur_socket)
            
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
        Reseau.serveur.broadcast("Nuit X", serveur_socket)

        # Les Loups-Garous choisissent une victime
        loups = [j for j in self.role if isinstance(j, Role.LoupGarou) and j.est_vivant]
        villageois = [j for j in self.role if not isinstance(j, Role.LoupGarou) and j.est_vivant]
        victime = None

        #A faire ps c comme les votes
        victime = self.interface.action(villageois, "Loup-Garou")   # choix des loupGarou ************************************
        victime = self.trouver_joueur(victime)
        for loup in loups:
            loup.attaquer(victime, self)

        # La Voyante sonde un joueur
        voyantes = [j for j in self.joueurs if isinstance(j, Role.Voyante) and j.est_vivant]
        if voyantes:
            Reseau.serveur.broadcast("Tour de la Vovo", serveur_socket)
            voyante = voyantes[0]
            Reseau.serveur.send("Role à voir",voyante.ip, serveur_socket)
            vu = server.handleClient()
            vu = self.trouver_joueur(vu)
            Reseau.serveur.send("Le role en question ct :" + vu.role ,voyante.ip, serveur_socket)


        # La Sorcière agit
        sorcieres = [j for j in self.joueurs if isinstance(j, Role.Sorciere) and j.est_vivant]
        if sorcieres:
            sorciere = sorcieres[0]
            if victime:  #choix de la sorcière************************************
                save = self.interface.action([victime], "Sorcière")
                if save:
                    sorciere.sauver(victime, self)
                
            
            cible = self.interface.action([j for j in self.joueurs if j != sorciere], "Sorcière") #choix de la sorcière************************************
            if cible:
                cible = self.trouver_joueur(cible)
                sorciere.tuer(cible, self)  

        self.nuit_numero += 1

    def tour_jour(self):
        self.jour = True
        self.votes = []
        self.chat("",f"\n--- Jour {self.nuit_numero} ---\n")
        
        variable_anti_mess_double=0
        for amoureux in self.amoureux:
            if not amoureux.est_vivant and variable_anti_mess_double==0:
                variable_anti_mess_double=-1
                self.chat("Maitre du jeu",f"{amoureux.nom} meurt, donc son amoureux {amoureux.amoureux.nom} se suicide.")
                amoureux.amoureux.mourir(self)
        

        self.afficher_joueurs()

        self.interface.chronometre(30)
        if self.votes:
            cible = self.votes[0]  #************************************
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

        self.interface.updateList(self.joueurs)
        self.phase_cupidon()
        self.phase_voleur()

        for _ in range(tours):
            # Vérifier s'il reste des Loup-Garous vivants
            loups_restants = any(isinstance(j, Role.LoupGarou) and j.est_vivant for j in self.joueurs)
            
            # Vérifier s'il reste des Villageois vivants
            villageois_restants = any(not isinstance(j, Role.LoupGarou) and j.est_vivant for j in self.joueurs)
    
            if loups_restants and villageois_restants:
                self.tour_nuit()
                self.tour_jour()
                self.afficher_joueurs()
    
            elif not villageois_restants:
                self.chat("Maitre du jeu","Les Loup-Garous ont gagné !")
    
            elif not loups_restants:
                self.chat("Maitre du jeu","Les villageois ont gagné !")
        self.chat("Maitre du jeu","La Partie est terminé, gg!")
        
        
