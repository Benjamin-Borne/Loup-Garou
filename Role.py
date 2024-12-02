# Classe de base Joueur
class Joueur:

    """
    Classe de base représentant un joueur.

    Attributs :
        nom (str) : Nom du joueur.
        est_vivant (bool) : Indique si le joueur est vivant.
        role (str) : Rôle du joueur (par défaut, None).

    Méthodes :
        __str__() : Retourne une représentation textuelle du joueur.
        mourir() : Marque le joueur comme mort et met à jour l'interface.
    """
    
    def __init__(self, nom):
    
        """
        Initialise un joueur.

        Input:
            nom (str) : Nom du joueur.
        """
        
        self.nom = nom
        self.est_vivant = True
        self.role = None

    def mourir(self, cycle):
        self.est_vivant = False
        cycle.chat("Maitre du jeu",f"{self.nom} ({self.role}) est mort.")
        cycle.afficher_joueurs()


# Classes spécifiques pour chaque rôle
class LoupGarou(Joueur):

    """
    Classe représentant un Loup-Garou.

    Méthodes :
        attaquer(joueur) : Attaque un joueur donné.
    """
    
    def __init__(self, nom):
        super().__init__(nom)
        self.role = "Loup-Garou"

    def attaquer(self, joueur, cycle):
        if joueur:
            if joueur.est_vivant:
                joueur.mourir(cycle)
                cycle.chat("Maitre du jeu",f"{self.nom} (Loup-Garou) attaque {joueur.nom}.")
        else:
            cycle.chat("Maitre du jeu",f"{self.nom} (Loup-Garou) n'attaque pas.")
                
            
class Voyante(Joueur):

    """
    Classe représentant une Voyante.

    Méthodes :
        sonder(joueur) : Découvre le rôle d'un joueur donné.
    """
    
    def __init__(self, nom):
        super().__init__(nom)
        self.role = "Voyante"

    def sonder(self, joueur, cycle):
        if joueur:
            cycle.chat("Maitre du jeu",f"{self.nom} (Voyante) sonde {joueur.nom}: {joueur.role}")
        else:
            cycle.chat("Maitre du jeu",f"{self.nom} (Voyante) ne sonde pas")
            
            
class Villageois(Joueur):

    """
    Classe représentant un Villageois.
    (Aucun pouvoir spécifique, rôle de base.)
    """
    
    def __init__(self, nom):
        super().__init__(nom)
        self.role = "Simple-Villageois"

class Sorciere(Joueur):

    """
    Classe représentant une Sorcière.

    Attributs :
        potion_vie (bool) : Indique si la potion de vie est disponible.
        potion_mort (bool) : Indique si la potion de mort est disponible.

    Méthodes :
        sauver(joueur) : Utilise la potion de vie sur un joueur.
        tuer(joueur) : Utilise la potion de mort sur un joueur.
    """
    
    def __init__(self, nom):
        super().__init__(nom)
        self.role = "Sorcière"
        self.potion_vie = True
        self.potion_mort = True

    def sauver(self, joueur, cycle):
        if self.potion_vie:
            joueur.est_vivant = True
            cycle.chat("Maitre du jeu",f"{self.nom} (Sorcière) utilise la potion de vie sur {joueur.nom}.")
            self.potion_vie = False

    def tuer(self, joueur, cycle):
        if self.potion_mort:
            cycle.chat("Maitre du jeu",f"{self.nom} (Sorcière) utilise la potion de mort sur {joueur.nom}.")
            joueur.mourir(cycle)
            self.potion_mort = False

class Chasseur(Joueur):

    """
    Classe représentant un Chasseur.

    Méthodes :
        tirer(cible) : Tire sur un joueur après sa mort.
        mourir() : Redéfinition pour déclencher l'action de tir.
    """
    
    def __init__(self, nom):
        super().__init__(nom)
        self.role = "Chasseur"

    def tirer(self, cible,cycle):
        if cible:
            if self.est_vivant is False:  # Tirer après la mort
                cycle.chat("Maitre du jeu",f"{self.nom} (Chasseur) tire sur {cible.nom}.")
                cible.mourir(cycle)
        else:
            cycle.chat("Maitre du jeu","Le chasseur n'a pas tiré")
    
    def mourir(self, cycle):
        super().mourir(cycle)
        self.tirer(cycle.trouver_joueur(cycle.interface.action(cycle.playerAlive(),"Chasseur")), cycle)

class Cupidon(Joueur):

    """
    Classe représentant Cupidon.

    Attributs :
        amoureux (list) : Liste des deux joueurs liés comme amoureux.

    Méthodes :
        lier_amoureux(joueur1, joueur2) : Lie deux joueurs comme amoureux.
    """
    
    def __init__(self, nom):
        super().__init__(nom)
        self.role = "Cupidon"
        self.amoureux = []  # Liste pour les amoureux

    def lier_amoureux(self, joueur1, joueur2, cycle):

        if joueur1 and joueur2:
            self.amoureux = [joueur1, joueur2]
            cycle.chat("Maitre du jeu",f"{self.nom} (Cupidon) lie {joueur1.nom} et {joueur2.nom} en tant qu'amoureux.")
            # Ajoute une référence pour savoir s'ils sont amoureux
            joueur1.amoureux = joueur2
            joueur2.amoureux = joueur1
        else:
            cycle.chat("Maitre du jeu","Aucun couple n'a été formé")

class Voleur(Joueur):

    """
    Classe représentant un Voleur.

    Attributs :
        peut_voler (bool) : Indique si le voleur peut encore voler un rôle.

    Méthodes :
        voler_role(joueur) : Vole le rôle d'un joueur donné.
    """
    
    def __init__(self, nom):
        super().__init__(nom)
        self.role = "Voleur"
        self.peut_voler = True  # Voleur peut voler une seule fois, durant la première nuit

    def voler_role(self, joueur, cycle):
        if not self.peut_voler:
            cycle.chat("Maitre du jeu",f"{self.nom} ne peut plus voler de rôle.")
            return
        if joueur == None:
            cycle.chat("Maitre du jeu","Aucun rôle n'a été volé.")
            return

        # Sélectionner aléatoirement un joueur dont le rôle va être volé
        cycle.chat("Maitre du jeu",f"{self.nom} vole le rôle de {joueur.nom} qui était {joueur.role}.")

        # Échange des rôles
        ancien_role = joueur.role
        joueur.role = "Voleur"  # La victime devient un Voleur sans la capacité de voler
        self.role = ancien_role  # Le voleur prend le rôle de la victime
        cycle.interface.changeImage(self.role)
        self.peut_voler = False  # Désactiver la capacité de voler
