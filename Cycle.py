# -*- coding: utf-8 -*-
import random
import Interface
import threading
import Role

localPlayer = 0

class Cycle:

    """
    Classe représentant la gestion du cycle jour/nuit.

    Attributs :
        joueurs (list) : Liste des joueurs participant à la partie.
        nuit_numero (int) : Compteur de tours de nuit.
        amoureux (list) : Liste des joueurs amoureux.
        voleur_role_choisi (bool) : Indique si le voleur a volé un rôle.
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
    
    def __init__(self, joueurs, interface):
    
        """
        Initialise un cycle de jeu.

        Args:
            joueurs (list) : Liste des joueurs participant à la partie.
        """
        self.interface = interface    
        self.joueurs = joueurs
        self.localPlayer = self.joueurs[localPlayer] #à modifier
        self.nuit_numero = 1
        self.amoureux = []
        self.voleur_role_choisi = False
        self.jour = False
        self.votes = []
        
    def trouver_joueur(self,nom):
        for joueur in self.joueurs:
            if joueur.nom == nom:
                return joueur
    def playerAlive(self):
        return [joueur for joueur in self.joueurs if joueur.est_vivant]

    def afficher_joueurs(self):
        vivants = []
        for joueur in self.joueurs:
            if joueur.est_vivant:
                vivants.append(joueur)
        self.interface.updateList(vivants)

    def chat(self, joueur = None, message = ""):
        if joueur is None:
            joueur = self.localPlayer.nom
        chatGui = self.interface.chatHistory
        pos = chatGui.index("end")
        chatGui.config(state='normal')
        if joueur == "Maitre du jeu":
            chatGui.insert(pos ,joueur + " : " + message + "\n", 'MDJ')
        else:
            if message == "":
                message = self.interface.entryMessage.get()
            if message != "":
                if joueur != "":
                    if self.jour:         
                        chatGui.insert(pos ,joueur + " : " + message + "\n")
                    else:
                        if self.trouver_joueur(joueur).role == "Loup-Garou":
                            chatGui.insert(pos ,joueur + " : " + message + "\n", "Loup-Garou")
                else:
                    chatGui.insert(pos , message + "\n")
        chatGui.config(state='disabled')
        chatGui.delete(0)
                
    def vote(self):
        if self.jour:
            if self.interface.listePlayers.curselection():
                voted = self.interface.listePlayers.get(first=self.interface.listePlayers.curselection()[0])
                self.interface.chatHistory.config(state='normal')
                self.chat(self.interface.local.nom, "Je vote contre : " + voted)
                self.interface.chatHistory.config(state='disabled')
                self.votes.append(self.trouver_joueur(voted))
                self.interface.listePlayers.selection_clear(0)


    def phase_cupidon(self):
        self.chat("Maitre du jeu","Tour du Cupidon")
        cupidon = None
        for j in self.joueurs:
            if isinstance(j, Role.Cupidon):
                cupidon = j
                break 
            
        joueur1 = self.interface.action(self.joueurs, "Cupidon")
        joueur2 = self.interface.action(self.joueurs, "Cupidon")
        if joueur1 and joueur2 and joueur1 != joueur2:
            joueur1 = self.trouver_joueur(joueur1)
            joueur2 = self.trouver_joueur(joueur2)
            cupidon.lier_amoureux(joueur1, joueur2, self)
            self.amoureux = [joueur1, joueur2]
        
        
    def phase_voleur(self):
        self.chat("Maitre du jeu","Tour du Voleur")
        voleur = None
        for j in self.joueurs:
            if isinstance(j, Role.Voleur) and j.peut_voler:
                voleur = j
        if self.nuit_numero == 1:
            volable = []
            for i in self.joueurs:
                if i.role != "Voleur":
                    volable.append(i)

            voler = self.interface.action(volable, "Voleur")
            voler = self.trouver_joueur(voler)
            voleur.voler_role(voler, self)

    def tour_nuit(self):
        """
        Exécute un tour de nuit :
        - Les Loups-Garous choisissent une victime.
        - La Voyante sonde un joueur.
        - La Sorcière agit (potion de vie ou de mort).

        Met à jour les statuts des joueurs en fonction des actions effectuées.
        """
        self.jour = False
        self.chat("",f"\n--- Nuit {self.nuit_numero} ---\n")


        # Les Loups-Garous choisissent une victime
        loups = [j for j in self.joueurs if isinstance(j, Role.LoupGarou) and j.est_vivant]
        villageois = [j for j in self.joueurs if not isinstance(j, Role.LoupGarou) and j.est_vivant]



        victime = None
        
        if loups:
            victime = self.interface.action(villageois, "Loup-Garou")   # choix des loupGarou ************************************
            victime = self.trouver_joueur(victime)
            for loup in loups:
                loup.attaquer(victime, self)

        # La Voyante sonde un joueur
        voyantes = [j for j in self.joueurs if isinstance(j, Role.Voyante) and j.est_vivant]
        if voyantes:
            voyante = voyantes[0]
            cible = self.trouver_joueur(self.interface.action(self.joueurs, "Voyante"))  #************************************
            voyante.sonder(cible, self)

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
                break
    
            elif not loups_restants:
                self.chat("Maitre du jeu","Les villageois ont gagné !")
                break
        self.chat("Maitre du jeu","La Partie est terminé, gg!")




#joueurs = création_des_joueurs(11)
# Création du cycle
joueurs = [
    Role.LoupGarou("Lucien"),
    Role.LoupGarou("Adrien"),
    Role.LoupGarou("Emma"),
    Role.Voyante("Louis"),
    Role.Sorciere("Benjamin"),
    Role.Villageois("Charlotte"),
    Role.Villageois("Lilou"),
    Role.Villageois("Titouan"),
    Role.Chasseur("Victor"),
    Role.Cupidon("Kevin"),
    Role.Voleur("Romain")
]
vivants = joueurs



interface = Interface.mainInterface(joueurs, joueurs[localPlayer]) 


jeu = Cycle(joueurs, interface)
interface.sendVote.configure(command=jeu.vote)
interface.sendChat.configure(command=jeu.chat)



# Lancer le cycle jour/nuit pour 10 tours
t = threading.Thread(target=jeu.lancer_cycle, args=[10])
t.start()
test = threading.Thread(target=interface.mainloop)
test.run()
