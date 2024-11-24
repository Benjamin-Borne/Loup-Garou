# -*- coding: utf-8 -*-
import random
import Interface
import threading


# Classe de base Joueur
class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.est_vivant = True
        self.role = None

    def __str__(self):
        return f"{self.nom} ({self.role})"

    def mourir(self):
        self.est_vivant = False
        jeu.chat("Maitre du jeu",f"{self.nom} ({self.role}) est mort.")
        jeu.afficher_joueurs()


# Classes spécifiques pour chaque rôle
class LoupGarou(Joueur):
    def __init__(self, nom):
        super().__init__(nom)
        self.role = "Loup-Garou"

    def attaquer(self, joueur):
        if joueur:
            if joueur.est_vivant:
                joueur.mourir()
                jeu.chat("Maitre du jeu",f"{self.nom} (Loup-Garou) attaque {joueur.nom}.")
        else:
            jeu.chat("Maitre du jeu",f"{self.nom} (Loup-Garou) n'attaque pas.")
                
            
class Voyante(Joueur):
    def __init__(self, nom):
        super().__init__(nom)
        self.role = "Voyante"

    def sonder(self, joueur):
        if joueur:
            jeu.chat("Maitre du jeu",f"{self.nom} (Voyante) sonde {joueur.nom}: {joueur.role}")
        else:
            jeu.chat("Maitre du jeu",f"{self.nom} (Voyante) ne sonde pas")
class Villageois(Joueur):
    def __init__(self, nom):
        super().__init__(nom)
        self.role = "Villageois"

class Sorciere(Joueur):
    def __init__(self, nom):
        super().__init__(nom)
        self.role = "Sorcière"
        self.potion_vie = True
        self.potion_mort = True

    def sauver(self, joueur):
        if self.potion_vie:
            joueur.est_vivant = True
            jeu.chat("Maitre du jeu",f"{self.nom} (Sorcière) utilise la potion de vie sur {joueur.nom}.")
            self.potion_vie = False

    def tuer(self, joueur):
        if self.potion_mort:
            jeu.chat("Maitre du jeu",f"{self.nom} (Sorcière) utilise la potion de mort sur {joueur.nom}.")
            joueur.mourir()
            self.potion_mort = False

class Chasseur(Joueur):
    def __init__(self, nom):
        super().__init__(nom)
        self.role = "Chasseur"

    def tirer(self, cible):
        if cible:
            if self.est_vivant is False:  # Tirer après la mort
                jeu.chat("Maitre du jeu",f"{self.nom} (Chasseur) tire sur {cible.nom}.")
                cible.mourir()
        else:
            jeu.chat("Maitre du jeu","Le chasseur n'a pas tiré")
    
    def mourir(self):
        super().mourir()
        self.tirer(jeu.trouver_joueur(interface.action(jeu.playerAlive(),"Chasseur")))

class Cupidon(Joueur):
    def __init__(self, nom):
        super().__init__(nom)
        self.role = "Cupidon"
        self.amoureux = []  # Liste pour les amoureux

    def lier_amoureux(self, joueur1, joueur2):

        if joueur1 and joueur2:
            self.amoureux = [joueur1, joueur2]
            jeu.chat("Maitre du jeu",f"{self.nom} (Cupidon) lie {joueur1.nom} et {joueur2.nom} en tant qu'amoureux.")
            # Ajoute une référence pour savoir s'ils sont amoureux
            joueur1.amoureux = joueur2
            joueur2.amoureux = joueur1
        else:
            jeu.chat("Maitre du jeu","Aucun couple n'a été formé")

class Voleur(Joueur):
    def __init__(self, nom):
        super().__init__(nom)
        self.role = "Voleur"
        self.peut_voler = True  # Voleur peut voler une seule fois, durant la première nuit

    def voler_role(self, joueur):
        if not self.peut_voler:
            jeu.chat("Maitre du jeu",f"{self.nom} ne peut plus voler de rôle.")
            return
        if joueur == None:
            jeu.chat("Maitre du jeu","Aucun rôle n'a été volé.")
            return

        # Sélectionner aléatoirement un joueur dont le rôle va être volé
        jeu.chat("Maitre du jeu",f"{self.nom} vole le rôle de {joueur.nom} qui était {joueur.role}.")

        # Échange des rôles
        ancien_role = joueur.role
        joueur.role = "Voleur"  # La victime devient un Voleur sans la capacité de voler
        self.role = ancien_role  # Le voleur prend le rôle de la victime
        interface.changeImage(self.role)
        self.peut_voler = False  # Désactiver la capacité de voler

joueurs = [
    LoupGarou("Lucien"),
    LoupGarou("Adrien"),
    LoupGarou("Emma"),
    Voyante("Louis"),
    Sorciere("Benjamin"),
    Villageois("Charlotte"),
    Villageois("Lilou"),
    Villageois("Titouan"),
    Chasseur("Victor"),
    Cupidon("Kevin"),
    Voleur("Romain")
]
vivants = joueurs

localPlayer = joueurs[0]



class Cycle:
    def __init__(self, joueurs):
        self.joueurs = joueurs
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
        interface.updateList(vivants)

    def chat(self, joueur = localPlayer, message = ""):
        chatGui = interface.chatHistory
        pos = chatGui.index("end")
        if message == "":
            message = interface.entryMessage.get()
        if message != "":
            chatGui.config(state='normal')
            if joueur != "":         
                chatGui.insert(pos ,joueur + " : " + message + "\n")
            else:
                chatGui.insert(pos , message + "\n")
            chatGui.config(state='disabled')
            chatGui.delete(0)
                
    def vote(self):
        if self.jour:
            if interface.listePlayers.curselection():
                voted = interface.listePlayers.get(first=interface.listePlayers.curselection()[0])
                interface.chatHistory.config(state='normal')
                self.chat(interface.local.nom, "Je vote contre : " + voted)
                interface.chatHistory.config(state='disabled')
                self.votes.append(self.trouver_joueur(voted))
                interface.listePlayers.selection_clear(0)


    def phase_cupidon(self):
        self.chat("Maitre du jeu","Tour du Cupidon")
        cupidon = None
        for j in self.joueurs:
            if isinstance(j, Cupidon):
                cupidon = j
                break 
            
        autres_joueurs = [j for j in self.joueurs ]
        joueur1 = interface.action(joueurs, "Cupidon")
        #joueur1, joueur2 = random.sample(autres_joueurs, 2)  # il faudra faire en sorte de faire choisir le cupidon *********
        cupidon.lier_amoureux(joueur1, joueur1)
        if joueur1: # à modifier
            self.amoureux = [joueur1, joueur1]
        
        
    def phase_voleur(self):
        self.chat("Maitre du jeu","Tour du Voleur")
        voleur = None
        for j in self.joueurs:
            if isinstance(j, Voleur) and j.peut_voler:
                voleur = j
                break
        if self.nuit_numero == 1:
            volable = []
            for i in self.joueurs:
                if i.role != "Voleur":
                    volable.append(i)

            voler = interface.action(volable, "Voleur")
            voler = self.trouver_joueur(voler)
            voleur.voler_role(voler)

    def tour_nuit(self):
        self.jour = False
        self.chat("",f"\n--- Nuit {self.nuit_numero} ---\n")

        
        # Les Loups-Garous choisissent une victime
        loups = [j for j in self.joueurs if isinstance(j, LoupGarou) and j.est_vivant]
        villageois = [j for j in self.joueurs if not isinstance(j, LoupGarou) and j.est_vivant]


        
        victime = None
        if loups:
            victime = interface.action(villageois, "Loup-Garou")   # choix des loupGarou ************************************
            victime = self.trouver_joueur(victime)
            for loup in loups:
                loup.attaquer(victime)

        # La Voyante sonde un joueur
        voyantes = [j for j in self.joueurs if isinstance(j, Voyante) and j.est_vivant]
        if voyantes:
            voyante = voyantes[0]
            interface.updateRoleAction(self.joueurs, "Voyante")
            cible = self.trouver_joueur(interface.action(self.joueurs, "Voyante"))  #************************************
            voyante.sonder(cible)
        
        # La Sorcière agit
        sorcieres = [j for j in self.joueurs if isinstance(j, Sorciere) and j.est_vivant]
        if sorcieres:
            sorciere = sorcieres[0]
            if victime and random.choice([True, False]):  #choix de la sorcière************************************
                sorciere.sauver(victime)
                
            else:
                cible = random.choice([j for j in self.joueurs if j != sorciere])  #choix de la sorcière************************************
                interface.updateRoleAction(self.joueurs, "Sorcière")
                sorciere.tuer(joueurs[8])  

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
                amoureux.amoureux.mourir()
        

        self.afficher_joueurs()

        interface.chronometre(30)
        if self.votes:
            cible = self.votes[0]  #************************************
            self.chat("Maitre du jeu",f"Les villageois votent pour éliminer {cible.nom}.")
            cible.mourir()
        else:
            self.chat("Maitre du jeu","Les villageois votent pour n'éliminer personne")

    def lancer_cycle(self, tours):
        # Phase Cupidon avant la première nuit
        
        interface.updateList(joueurs)
        self.phase_cupidon()
        self.phase_voleur()

        for _ in range(tours):
            # Vérifier s'il reste des Loup-Garous vivants
            loups_restants = any(isinstance(j, LoupGarou) and j.est_vivant for j in self.joueurs)
            
            # Vérifier s'il reste des Villageois vivants
            villageois_restants = any(not isinstance(j, LoupGarou) and j.est_vivant for j in self.joueurs)
    
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



jeu = Cycle(joueurs)


interface = Interface.mainInterface(joueurs, localPlayer) 

interface.sendVote.configure(command=jeu.vote)
interface.sendChat.configure(command=jeu.chat)

# Lancer le cycle jour/nuit pour 10 tours
t = threading.Thread(target=jeu.lancer_cycle, args=[10])
t.start()
test = threading.Thread(target=interface.mainloop)
test.run()
