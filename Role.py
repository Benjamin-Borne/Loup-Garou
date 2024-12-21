# Classe de base Joueur
class Joueur:

    """
    Classe de base représentant un joueur.

    Attributs :
        nom (str) : Nom du joueur.
        est_vivant (bool) : Indique si le joueur est vivant.
        role (str) : Rôle du joueur (par défaut, None).

    Méthodes :
        mourir() : Marque le joueur comme mort.
    """
    
    def __init__(self):
    
        """
        Initialise un joueur.
        """
        
        self.nom = ""
        self.est_vivant = True
        self.role = None

    def mourir(self):
        self.est_vivant = False

    def agir(self, joueurs, interface):
        cibles = joueurs[:]
        cibles.remove(self.nom)
        cible = interface.action(cibles)
        return cible


# Classes spécifiques pour chaque rôle
class LoupGarou(Joueur):

    """
    Classe représentant un Loup-Garou.
    """
    
    def __init__(self):
        super().__init__()
        self.role = "Loup-Garou"

                
            
class Voyante(Joueur):

    """
    Classe représentant une Voyante.
    """
    
    def __init__(self):
        super().__init__()
        self.role = "Voyante"

            
            
class Villageois(Joueur):

    """
    Classe représentant un Villageois.
    (Aucun pouvoir spécifique, rôle de base.)
    """
    
    def __init__(self):
        super().__init__()
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
    
    def __init__(self):
        super().__init__()
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
    """
    
    def __init__(self):
        super().__init__()
        self.role = "Chasseur"

class Cupidon(Joueur):

    """
    Classe représentant Cupidon.

    Méthodes :
        agir(self, joueurs, interface) : Permet au cupidon de choisir les deux amoureux parmis la liste des joueurs.
    """
    
    def __init__(self):
        super().__init__()
        self.role = "Cupidon"

    def agir(self, joueurs, interface):
        cibles = joueurs[:]
        amoureux1 = interface.action(cibles)
        cibles.remove(amoureux1)
        amoureux2 = interface.action(cibles)
        if amoureux1 and amoureux2:
            return amoureux1,amoureux2
        return None

class Voleur(Joueur):

    """
    Classe représentant un Voleur.
    """
    
    def __init__(self):
        super().__init__()
        self.role = "Voleur"
        
   

def createPlayer(role, name):
    """
        Renvoie un objet de la classe Joueur en fonction d'un role et du pseudo.

        Input:
            role (str): Nom du role.
            name (str): Nom du joueur.

        Output:
            (Joueur) : Object créé en fonction des paramètres, ou None si le rôle n'existe pas.
    """

    player = None
    match role:
        case "Voleur":
            player = Voleur()
        case "Cupidon":
            player = Cupidon()
        case "Sorcière":
            player = Sorciere()
        case "Chasseur":
            player = Chasseur()
        case "Voyante":
            player = Voyante()
        case "Loup-Garou":
            player = LoupGarou()
        case "Simple-Villageois":
            player = Villageois()
    
    if player:
        player.nom = name
        return player
    return None
