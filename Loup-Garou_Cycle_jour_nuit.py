# -*- coding: utf-8 -*-
import random

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
        print(f"{self.nom} est mort.")

# Classes spécifiques pour chaque rôle
class LoupGarou(Joueur):
    def __init__(self, nom):
        super().__init__(nom)
        self.role = "Loup-Garou"

    def attaquer(self, joueur):
        if joueur.est_vivant:
            joueur.mourir()
            print(f"{self.nom} (Loup-Garou) attaque {joueur.nom}.")
            

class LoupGarouBlanc(LoupGarou):
    def __init__(self, nom):
        super().__init__(nom)
        self.is_white = True  # Le Loup-Garou Blanc est un Loup-Garou spécial

    def attaquer(self, cible):
        if cible.est_vivant:
            
            
            
class Voyante(Joueur):
    def __init__(self, nom):
        super().__init__(nom)
        self.role = "Voyante"

    def sonder(self, joueur):
        print(f"{self.nom} (Voyante) sonde {joueur.nom}: {joueur.role}")

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
            print(f"{self.nom} (Sorcière) utilise la potion de vie sur {joueur.nom}.")
            self.potion_vie = False

    def tuer(self, joueur):
        if self.potion_mort:
            joueur.mourir()
            print(f"{self.nom} (Sorcière) utilise la potion de mort sur {joueur.nom}.")
            self.potion_mort = False

class Chasseur(Joueur):
    def __init__(self, nom):
        super().__init__(nom)
        self.role = "Chasseur"

    def tirer(self, cible):
        if self.est_vivant is False:  # Tirer après la mort
            print(f"{self.nom} (Chasseur) tire sur {cible.nom}.")
            cible.mourir()
            

class Cupidon(Joueur):
    def __init__(self, nom):
        super().__init__(nom)
        self.role = "Cupidon"
        self.amoureux = []  # Liste pour les amoureux

    def lier_amoureux(self, joueur1, joueur2):
        self.amoureux = [joueur1, joueur2]
        print(f"{self.nom} (Cupidon) lie {joueur1.nom} et {joueur2.nom} en tant qu'amoureux.")
        # Ajoute une référence pour savoir s'ils sont amoureux
        joueur1.amoureux = joueur2
        joueur2.amoureux = joueur1

class Voleur(Joueur):
    def __init__(self, nom):
        super().__init__(nom)
        self.role = "Voleur"
        self.peut_voler = True  # Voleur peut voler une seule fois, durant la première nuit

    def voler_role(self, joueurs):
        if not self.peut_voler:
            print(f"{self.nom} ne peut plus voler de rôle.")
            return

        # Filtrer les joueurs dont le rôle peut être volé (excluant le Voleur lui-même)
        joueurs_volables = [j for j in joueurs if j.role != "Voleur" and j.est_vivant]

        if not joueurs_volables:
            print("Aucun rôle ne peut être volé.")
            return

        # Sélectionner aléatoirement un joueur dont le rôle va être volé
        victime = random.choice(joueurs_volables)
        print(f"{self.nom} vole le rôle de {victime.nom} qui était {victime.role}.")

        # Échange des rôles
        ancien_role = victime.role
        victime.role = "Voleur"  # La victime devient un Voleur sans la capacité de voler
        self.role = ancien_role  # Le voleur prend le rôle de la victime
        self.peut_voler = False  # Désactiver la capacité de voler

       
class Cycle:
    def __init__(self, joueurs):
        self.joueurs = joueurs
        self.nuit_numero = 1
        self.amoureux = []
        self.voleur_role_choisi = False

    def afficher_joueurs(self):
        vivants = []
        for joueur in self.joueurs:
            if joueur.est_vivant:
                vivants.append(joueur)
        print("\n *************************")
        print("\nLes joueurs encore en vie :")
        for joueur in vivants:
            print(joueur)
        print("\n *************************")

    def phase_cupidon(self):
        cupidon = None
        for j in self.joueurs:
            if isinstance(j, Cupidon):
                cupidon = j
                break 
            
        autres_joueurs = [j for j in self.joueurs ]
        joueur1, joueur2 = random.sample(autres_joueurs, 2)  # il faudra faire en sorte de faire choisir le cupidon *********
        cupidon.lier_amoureux(joueur1, joueur2)
        self.amoureux = [joueur1, joueur2]
        
        
    def phase_voleur(self):
    
        voleur = None
        for j in self.joueurs:
            if isinstance(j, Voleur) and j.peut_voler:
                voleur = j
                print (voleur)
                break
        if voleur and self.nuit_numero == 1:
            voleur.voler_role(self.joueurs)







    def tour_nuit(self):
        print(f"\n--- Nuit {self.nuit_numero} ---")

        
        # Les Loups-Garous choisissent une victime
        loups = [j for j in self.joueurs if isinstance(j, LoupGarou) and j.est_vivant]
        villageois = [j for j in self.joueurs if not isinstance(j, LoupGarou) and j.est_vivant]
        
        victime = None
        if loups:
            victime = random.choice(villageois)   # choix des loupGarou ************************************
            for loup in loups:
                loup.attaquer(victime)

        # La Voyante sonde un joueur
        voyantes = [j for j in self.joueurs if isinstance(j, Voyante) and j.est_vivant]
        if voyantes:
            voyante = voyantes[0]
            cible = random.choice(self.joueurs)  #************************************
            voyante.sonder(cible)
        
        # La Sorcière agit
        sorcieres = [j for j in self.joueurs if isinstance(j, Sorciere) and j.est_vivant]
        if sorcieres:
            sorciere = sorcieres[0]
            if victime and random.choice([True, False]):  #choix de la sorcière************************************
                sorciere.sauver(victime)
                
            else:
                cible = random.choice([j for j in self.joueurs if j != sorciere])  #choix de la sorcière************************************
                sorciere.tuer(cible)  



        self.nuit_numero += 1

    def tour_jour(self):
        print(f"\n--- Jour {self.nuit_numero} ---")
        
        variable_anti_mess_double=0
        for amoureux in self.amoureux:
            if not amoureux.est_vivant and variable_anti_mess_double==0:
                variable_anti_mess_double=-1
                print(f"{amoureux.nom} meurt, donc son amoureux {amoureux.amoureux.nom} se suicide.")
                amoureux.amoureux.mourir()
        

        self.afficher_joueurs()
        
        
        vivants = [j for j in self.joueurs if j.est_vivant]
        cible = random.choice(vivants)  # faudra faire en sorte que ce soit le choix des joueurs ************************************
        print(f"Les villageois votent pour éliminer {cible.nom}.")
        
        
        # Le chasseur tire avant de mourir
        if isinstance(cible, Chasseur):
            cible.mourir()
            cible.tirer(random.choice(vivants))   # choix chasseur ************************************
        else:
            cible.mourir()

    def lancer_cycle(self, tours):
        # Phase Cupidon avant la première nuit
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
                print("Les Loup-Garous ont gagné !")
                break
    
            elif not loups_restants:
                print("Les villageois ont gagné !")
                break
        print("La Partie est terminer, gg!")
"""         
 '''           
def création_des_joueurs(nb_de_j):
    assert (nb_de_j>7 and nb_de_j<16)
    roles_uniques = [
        Voyante("Voyante"),
        Sorciere("Sorcière"),
        Chasseur("Chasseur"),
        Cupidon("Cupidon"),
        Voleur("Voleur")
    ]
    roles = [
        LoupGarou("Loup-Garou 1"),
        Villageois("Villageois 1")
    if nb_de_j==8:
        joueurs = [
            LoupGarou("Lucien"),
            LoupGarou("Adrien"),
            Voyante("Louis"),
            Sorciere("Benjamin"),
            Villageois("Charlotte"),
            Villageois("Lilou"),
            Villageois("Titouan"),
            Chasseur("Victor")
        ]
    
    if nb_de_j==9:
        joueurs = [
            LoupGarou("Lucien"),
            LoupGarou("Adrien"),
            Voyante("Louis"),
            Sorciere("Benjamin"),
            Villageois("Charlotte"),
            Villageois("Lilou"),
            Villageois("Titouan"),
            Chasseur("Victor"),
            Voleur("Ernest")
        ]

    if nb_de_j==10:
        joueurs = [
            LoupGarou("Lucien"),
            LoupGarou("Adrien"),
            Voyante("Louis"),
            Sorciere("Benjamin"),
            Villageois("Charlotte"),
            Villageois("Lilou"),
            Villageois("Titouan"),
            Chasseur("Victor"),
            Cupidon("Kevin"),
            Voleur("Ernest")
        ]
        
    if nb_de_j==11:
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
            Voleur("Ernest")
        ]

    if nb_de_j==12:
        joueurs = [
            LoupGarou("Lucien"),
            LoupGarou("Adrien"),
            LoupGarou("Emma"),
            Voyante("Louis"),
            Sorciere("Benjamin"),
            Villageois("Charlotte"),
            Villageois("Lilou"),
            Villageois("Titouan"),
            Villageois("Noa"),
            Chasseur("Victor"),
            Cupidon("Kevin"),
            Voleur("Ernest")
        ]
    
    if nb_de_j==13:
        joueurs = [
            LoupGarou("Lucien"),
            LoupGarou("Adrien"),
            LoupGarou("Emma"),
            LoupGarou("Olivier"),
            Voyante("Louis"),
            Sorciere("Benjamin"),
            Villageois("Charlotte"),
            Villageois("Lilou"),
            Villageois("Titouan"),
            Villageois("Noa"),
            Chasseur("Victor"),
            Cupidon("Kevin"),
            Voleur("Ernest")
        ]

    if nb_de_j==14:
        joueurs = [
            LoupGarou("Lucien"),
            LoupGarou("Adrien"),
            LoupGarou("Emma"),
            LoupGarou("Olivier"),
            LoupGarouBlanc("Lucie"),
            Voyante("Louis"),
            Sorciere("Benjamin"),
            Villageois("Charlotte"),
            Villageois("Lilou"),
            Villageois("Titouan"),
            Villageois("Noa"),
            Chasseur("Victor"),
            Cupidon("Kevin"),
            Voleur("Ernest")
        ]
        
        
    if nb_de_j==15:
        
    if nb_de_j==16:
    
    if nb_de_j==17:

    if nb_de_j==18:
        
        
        
    random.shuffle(roles_uniques)
    joueurs=[]*nb_de_j 
    for i in range(len(roles_uniques)):
        joueurs[i]=roles_uniques[i]
    for j in range (nb_de_j-len(roles_uniques)):
        choixxx=random(0,1)
        joueurs[j+5]=roles[choixxx]
    return joueurs
   ''' 
"""

         
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
    Voleur("Ernest")
]


#joueurs = création_des_joueurs(11)
# Création du cycle
jeu = Cycle(joueurs)

# Lancer le cycle jour/nuit pour 10 tours
jeu.lancer_cycle(100)