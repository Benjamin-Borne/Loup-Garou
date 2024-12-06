import tkinter as tk
from tkinter import scrolledtext
from PIL import ImageTk
from PIL import Image
import time

def false():
    """
    Fonction utilitaire qui retourne False.
    Utilisée comme condition par défaut pour certaines méthodes.
    """
    return False


class mainInterface(tk.Tk):

    """
    Classe principale pour l'interface graphique du jeu Loup-Garou.
    Hérite de la classe tk.Tk et gère :
    - Le chat
    - La liste des joueurs
    - L'affichage du rôle
    - Les actions spécifiques aux rôles
    - Le chronomètre
    """
    
    def __init__(self, playersList, localPlayer):
    
        """
        Initialise l'interface principale.

        Input:
            playersList (list): Liste des joueurs.
            localPlayer (object): Joueur local.
        """
            
        tk.Tk.__init__(self)
        self.local = localPlayer
        self.role = self.local.role
        self.frameChat = tk.Frame(self, bg="#848484", width=400)
        self.chatHistory = scrolledtext.ScrolledText(self.frameChat, wrap=tk.WORD, state='disabled')
        self.entryFrame = tk.Frame(self.frameChat)
        self.entryMessage = tk.Entry(self.entryFrame, width=54)
        self.leftFrame = tk.Frame(self, bg="#3396c7")
        self.framePlayer = tk.Frame(self.leftFrame, width=400, height=600, bg="lightblue")
        self.listePlayers = tk.Listbox(self.framePlayer, height=25, width=40, selectmode="single")
        self.chronoGUI = tk.Label(self.leftFrame, text="Liste des joueurs", font=("Arial", 14), bg="lightblue")
        self.players = [playersList[i].nom for i in range(len(playersList))]

        self.roleActionFrame = tk.Frame(self, bg="#3396c7")
        self.roleAction = tk.Listbox(self.roleActionFrame, height=25, width=40, selectmode="single")
        self.roleAction.pack()

        self.frameChat.pack_propagate(False)
        self.frameChat.pack(side=tk.RIGHT, padx=10, pady=10, fill="y")

        self.roleActionFrame.pack(side="right")

        self.img = Image.open("ressources/loup-garou-dos"+".png")
        self.img = self.img.resize((200,200))
        self.img = ImageTk.PhotoImage(self.img,(100,100))

        self.title("Loup Garou")
        self.iconphoto(True,self.img)
        self.config(background="#3396c7")
        self.minsize(975,650)

        self.chatHistory.pack(expand="yes", fill="both")

        self.chatHistory.tag_config("Loup-Garou", foreground="red")
        self.chatHistory.tag_config("MDJ", foreground="purple")

        self.entryFrame.pack()
        self.entryMessage.pack(side='left')

        self.sendChat = tk.Button(self.entryFrame, text="Envoyer", width=10)
        self.sendChat.pack(side="right")

        self.leftFrame.pack(side=tk.LEFT)
        self.chronoGUI.pack(side ="top")
        
        self.framePlayer.pack(side="bottom", padx=20)

        labelPlayer = tk.Label(self.framePlayer, text="Liste des joueurs", font=("Arial", 14), bg="lightblue")
        labelPlayer.pack(pady=10)

        self.listePlayers.pack(pady=10)
        
        self.sendVote = tk.Button(self.framePlayer, text="Voter", width=10)
        self.sendVote.pack()

        self.frameRole = tk.Frame(self.leftFrame, bg="#3396c7")
        self.frameRole.pack(side="top", pady=20)
        
        self.roleImg = tk.Label(self.frameRole, image=self.img, bg ="#3396c7")
        self.roleTxt = tk.Label(self.frameRole, text=None, bg="#3396c7",font=("Arial", 28), fg="white")
        self.roleImg.pack(side="bottom")
        self.roleTxt.pack(expand="yes", fill="both", side="top")
    
        self.changeImage(self.role)

    def changeImage(self,role):
    
        """
        Change l'image et le texte associés au rôle.

        Input:
            role (str): Nom du rôle actuel.
        """
        
        self.img = Image.open("ressources/"+role.lower()+".png")
        self.img = self.img.resize((200,200))
        self.img = ImageTk.PhotoImage(self.img,(100,100))

        self.roleImg.configure(image=self.img)
        self.roleTxt.configure(text=role)

        self.role = role
    

    def chat(self, joueur, message = ""):
    
        """
        Ajoute un message au chat.

        Input:
            joueur (str): Nom du joueur qui envoie le message (vide pour les messages globaux).
            message (str): Contenu du message. Si vide, prend le contenu de `entryMessage`.
        """
        
        if message == "":
            message = self.entryMessage.get()
        if message != "":
            if joueur != "":
                self.chatHistory.config(state='normal')
                self.chatHistory.insert(tk.END, joueur + " : " + message + "\n")
                self.chatHistory.config(state='disabled')
                self.entryMessage.delete(0, tk.END)
            else:
                self.chatHistory.config(state='normal')
                self.chatHistory.insert(tk.END, message + "\n")
                self.chatHistory.config(state='disabled')
                self.entryMessage.delete(0, tk.END)

    def chronometre(self, temps, condition = false):
    
        """
        Lance un compte à rebours.

        Args:
            temps (int): Temps en secondes pour le compte à rebours.
            condition (function): Fonction qui retourne True pour arrêter le chronomètre prématurément.
        """
        
        for i in range(temps,0,-1):
            if not condition():
                self.chronoGUI.configure(text = str(i))
                time.sleep(1)
            else:
                self.chronoGUI.configure(text = "0")
                return


    def updateList(self, playerAlive):
    
        """
        Met à jour la liste des joueurs affichés, indiquant ceux qui sont morts.

        Input:
            playerAlive (list): Liste des joueurs vivants, chaque joueur ayant un attribut `nom`.
        """
        
        playersAlive = [playerAlive[i].nom for i in range(len(playerAlive))]
        self.listePlayers.delete(0, self.listePlayers.size())
        for player in self.players:
            if player in playersAlive:
                self.listePlayers.insert(tk.END, player)
            else:
                self.listePlayers.insert(tk.END, player + " (mort)")
    
    def updateRoleAction(self, affectedPlayers, roleName):
    
        """
        Met à jour la liste des actions disponibles en fonction des joueurs affectés et du rôle.

        Input:
            affectedPlayers (list): Liste des joueurs concernés par l'action.
            roleName (str): Nom du rôle exécutant l'action.
        """
            
        if roleName == self.role:
            aPlayers = [affectedPlayers[i].nom for i in range(len(affectedPlayers))] + ["Ne rien faire"]
            self.roleAction.delete(0, self.listePlayers.size())
            for player in aPlayers:
                self.roleAction.insert(tk.END, player)

    def action(self, affectedPlayers, roleName): 
    
        """
        Réalise une action en fonction du rôle actuel et des joueurs affectés.

        Input:
            affectedPlayers (list): Liste des joueurs concernés par l'action.
            roleName (str): Nom du rôle exécutant l'action.

        Output:
            str: Nom du joueur sélectionné pour l'action, ou None si aucune action n'a été prise.
        """
         
        if self.local.role == roleName:
            self.updateRoleAction(affectedPlayers, roleName)
            self.roleAction.pack()
            self.chronometre(10,self.roleAction.curselection)
            if self.roleAction.curselection():
                player = self.roleAction.get(first=self.roleAction.curselection()[0])
                self.roleAction.pack_forget()
                if player == "Ne rien faire":
                    return None
                return player
        self.roleAction.pack_forget()
        return None       


