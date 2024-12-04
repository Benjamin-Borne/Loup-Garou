# Classe de base Joueur
class Joueur:

    """
    Classe de base représentant un joueur.

    Attributs :
        nom (str) : Nom du joueur.
        est_vivant (bool) : Indique si le joueur est vivant.
        role (str) : Rôle du joueur (par défaut, None).

    Méthodes :
        mourir() : Marque le joueur comme mort et met à jour l'interface.
    """
    
    def __init__(self):
    
        """
        Initialise un joueur.
        Constructeur par default
        """
        
        self.nom = ""
        self.est_vivant = True
        self.role = None
        self.ip=None

    def mourir(self):
        """
            tue le joueur
        """
        self.est_vivant = False


# Classes spécifiques pour chaque rôle
class LoupGarou(Joueur):

    """
    Classe représentant un Loup-Garou.

    Méthodes :
        attaquer(joueur) : Attaque un joueur donné.
    """
    
    def __init__(self):
        super().__init__()
        self.role = "Loup-Garou"
        
            
class Voyante(Joueur):

    """
    Classe représentant une Voyante.

    Méthodes :
        sonder(joueur) : Découvre le rôle d'un joueur donné.
    """
    
    def __init__(self):
        super().__init__()
        self.role = "Voyante"

    def sonder(self):
        """
            input : -- 
                    demande interface pour get cible de voyante !! Victor
            output : -- role de la cible (str)
        """
        cible = "choix de la voyante --> interface" #Victor
        return cible.role
  
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

    def sauver(self):
        """
            input: --
                    get cible a sauver par interface !! Victor
            output : maj de l'etat de la cible : vivant (True)
                     maj de la potion vie (False)
                     -- cible.nom (str)
        """
        cible = "choix de la sorciere --> interface (Joueur)" #Victor
        self.potion_vie=False
        cible.est_Vivant=True
        return cible.nom
        

    def tuer(self):
        """
            input: -- 
                    get cible a tuer par interface !! Victor 
            output : maj de l'etat de la cible : mort (False)
                     maj de la potion mort (False)
                     -- cible.nom (str)
        """
        cible = "choix de la sorciere --> interface (Joueur)" #Victor
        self.potion_mort=False
        cible.mourir()
        return cible.nom
        

class Chasseur(Joueur):

    """
    !!! A REVOIR !!!
    Classe représentant un Chasseur.

    Méthodes :
        tirer(cible) : Tire sur un joueur après sa mort.
        mourir() : Redéfinition pour déclencher l'action de tir. 
    """
    
    def __init__(self):
        super().__init__()
        self.role = "Chasseur"

    def tirer(self,cible):
        """
            input: -- cible a tuer (Joueur) 
            output : maj de l'etat de la cible : mort (False)
                     -- cible.nom (str)
        """
        cible.mourir()
        return cible.nom
    
    def mourir(self):
        """
            !!! A FAIRE !!!
            input: -- self : instance
                    get cible a tuer par interface !! Victor
            output : maj de l'etat du joueur : mort (False)
                     get cible du chasseur
                     appel la fonction tirer(cible) (Joueur)
                     -- 
                     
        """
        super().mourir()
        cible = "choix du chasseur --> interface (Joueur)" #Victor
        self.tirer(cible)

class Cupidon(Joueur):

    """
    Classe représentant Cupidon.

    Attributs :
        amoureux (list) : Liste des deux joueurs liés comme amoureux.

    Méthodes :
        lier_amoureux(joueur1, joueur2) : Lie deux joueurs comme amoureux.
    """
    
    def __init__(self):
        super().__init__()
        self.role = "Cupidon"
        self.amoureux = []  # Liste des amoureux

    def lier_amoureux(self):
        """
            input : -- self : instance
                        get joueur1 et joueur2 a lier par interface !! Victor
            output : set de self.amoureux avec les deux joueurs (liste)
                     set des amoureux des deux joueurs
                     -- tuple des nom des joueurs
        """
        joueur1 = "choix1 du cupidon --> interface (Joueur)" #Victor
        joueur2 = "choix2 du cupidon --> interface (Joueur)" #Victor

        self.amoureux=[joueur1,joueur2]
        joueur1.amoureux = joueur2
        joueur2.amoureux = joueur1
        return (self.amoureux[0].nom,self.amoureux[1].nom)

        

class Voleur(Joueur):

    """
    Classe représentant un Voleur.

    Attributs :
        peut_voler (bool) : Indique si le voleur peut encore voler un rôle.

    Méthodes :
        voler_role(joueur) : Vole le rôle d'un joueur donné.
    """
    
    def __init__(self):
        super().__init__()
        self.role = "Voleur"

    def voler_role(self):
        """
        input : -- self : instance
                echange des roles
        output : -- peut etre un return 
        """

        cible = "choix du voleur --> interface (Joueur)" #Victor
        role_cible=cible.role
        self.role=role_cible
        cible.role="Voleur"
        #changer les images des roles
        #peut etre un return... surprise!
        