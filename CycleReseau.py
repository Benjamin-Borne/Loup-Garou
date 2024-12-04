import Interface
import threading
import random
import Role
import Composition
#import Serveur

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
        self.IPjoueurs = Reseau.serveur.getClients()
        self.pseudo = Reseau.client.pseudo()
        self.role = Composition.createComp(len(self.pseudo))


        players = random.shuffle(self.pseudo[:])
        for i in range(len(players)):
            self.role[i].nom = players[i]
            self.role[i].ip = self.IPjoueurs[i]
            #Set up client

        self.nuit_numero = 0

        self.jour = False

        self.amoureux = []
        self.votes = []
        
    def trouver_joueur(self,nom):
        for joueur in self.role:
            if joueur.nom == nom:
                return joueur

    def playerAlive(self):
        return [joueur for joueur in self.role if joueur.est_vivant]
    

    def phase_cupidon(self):
        for j in self.role:
            if isinstance(j, Role.Cupidon):
                cupidon = j
        
        
        #Afficher message
        """
        format message:
                        #pseudo$data@typeAction
        """
        Reseau.serveur.broadcast("message", serveur_socket)
        #Cupidon choisis
        Reseau.serveur.send("CupidonChoix",cupidon.ip, serveur_socket)
        joueur1, joueur2 = server.handleClient(), server.handleClient()
        

        if joueur1 and joueur2 and joueur1 != joueur2:
            #serveur traite
            self.amoureux = [self.trouver_joueur(joueur1), self.trouver_joueur(joueur2)]
            #Message aux amoureux
            Reseau.serveur.send("T amoureux", self.amoureux[0].ip, serveur_socket)
            Reseau.serveur.send("Toi aussi lol", self.amoureux[1].ip, serveur_socket)
            Reseau.serveur.send("GG t'as fait un couple",cupidon.ip, serveur_socket)
        else:
            Reseau.serveur.send("Miskin y'a pas de couple",cupidon.ip, serveur_socket)
        
        
    def phase_voleur(self):
        Reseau.serveur.broadcast("message", serveur_socket)
        for player in self.role:
            if isinstance(player, Role.Voleur) and player.peut_voler:
                voleur = player
        if self.nuit_numero == 1:
            volable = []
            for player in self.role:
                if player.role != "Voleur":
                    volable.append(player)

            Reseau.serveur.broadcast("message", serveur_socket)
            Reseau.serveur.send("VoleurChoix",voleur.ip, serveur_socket)

            vole = server.handleClient()
            if vole:
                vole = self.trouver_joueur(vole)
                voleur.voler_role(vole)
                #Debrouiller pour changer image
                Reseau.serveur.send("T'as volé (changer image)",voleur.ip, serveur_socket)
                Reseau.serveur.send("T'as été volé (changer image)",vole.ip, serveur_socket)

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
