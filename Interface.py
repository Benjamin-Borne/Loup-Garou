import tkinter as tk
from tkinter import scrolledtext
from PIL import ImageTk
from PIL import Image
import time
import threading
import server

PETITE_FILLE_TEMPS = 5

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
    
    def __init__(self, playersList, role, client):
    
        """
        Initialise l'interface principale.

        Input:
            playersList (list): Liste des joueurs.
            localPlayer (object): Joueur local.
        """
        self.client = client
        
        tk.Tk.__init__(self)
        self.pf = False
        self.pfTime = PETITE_FILLE_TEMPS
        self.canChat = False
        self.loupChat = False
        self.start_receiving = False
        
        self.role = role
        self.title("Loup Garou")
        self.players = playersList
        self.lock = threading.Lock()

        #Initialisation des fenêtres
        
        #Création de l'image de rôle
        self.img = Image.open("ressources/loup-garou-dos"+".png")
        self.img = self.img.resize((200,200))
        self.img = ImageTk.PhotoImage(self.img,(100,100))
        self.iconphoto(True,self.img)
        
        self.frameChat = tk.Frame(self, bg="#848484", width=400)
        self.chatHistory = scrolledtext.ScrolledText(self.frameChat, wrap=tk.WORD, state='disabled')
        self.entryFrame = tk.Frame(self.frameChat)
        self.entryMessage = tk.Entry(self.entryFrame, width=30)
        self.leftFrame = tk.Frame(self, bg="#3396c7")
        self.frameRole = tk.Frame(self.leftFrame, bg="#3396c7")
        self.framePlayer = tk.Frame(self.leftFrame, width=400, height=600, bg="lightblue")
        self.listePlayers = tk.Listbox(self.framePlayer, height=25, width=40, selectmode="single")
        self.chronoGUI = tk.Label(self.leftFrame, text="Liste des joueurs", font=("Arial", 14), bg="lightblue")
        self.roleImg = tk.Label(self.frameRole, image=self.img, bg ="#3396c7")
        self.roleTxt = tk.Label(self.frameRole, text=None, bg="#3396c7",font=("Arial", 28), fg="white")
        labelPlayer = tk.Label(self.framePlayer, text="Liste des joueurs", font=("Arial", 14), bg="lightblue")
        self.config(background="#3396c7")
        self.minsize(975,650)

        #Initialisation des boutons
        self.sendChat = tk.Button(self.entryFrame, text="Envoyer", width=10, command=self.sendMessage)
        self.sendVote = tk.Button(self.framePlayer, text="Voter", width=10)

        #GUI pour les rôles
        self.roleActionFrame = tk.Frame(self, bg="#3396c7")
        #cas pour la petite-fille
        self.petiteFilleAction = tk.Button(self.roleActionFrame, height=25, width=40, fg='red', bg='red')
        self.petiteFilleAction.bind("<Button-1>", self.pfClick)
        self.petiteFilleAction.bind("<ButtonRelease-1>", self.pfRelease)
        #cas pour le reste
        self.roleAction = tk.Listbox(self.roleActionFrame, height=25, width=40, selectmode="single")



        #GUI pour le chat
        self.frameChat.pack_propagate(False)
        self.frameChat.pack(side=tk.RIGHT, padx=10, pady=10, fill="y")

        self.chatHistory.pack(expand="yes", fill="both")
        self.chatHistory.tag_config("Loup-Garou", foreground="red")
        self.chatHistory.tag_config("MDJ", foreground="purple")

        self.entryFrame.pack()
        self.entryMessage.pack(side='left')
        self.sendChat.pack(side="right")



        #Pack
        self.roleActionFrame.pack(side="right")
        self.leftFrame.pack(side=tk.LEFT)
        self.chronoGUI.pack(side ="top")
        self.roleImg.pack(side="bottom")
        self.roleTxt.pack(expand="yes", fill="both", side="top")
        self.framePlayer.pack(side="bottom", padx=20)
        labelPlayer.pack(pady=10)
        self.listePlayers.pack(pady=10)
        self.sendVote.pack()
        self.frameRole.pack(side="top", pady=20)

        #Set-up
        self.changeImage(self.role)
        self.updateList(self.players)

        self.withdraw()

    def startUpdates(self, usernames: list, role):
        self.players= usernames
        self.listePlayers.delete(0, tk.END)
        self.role = role
        for user in self.players:
            self.listePlayers.insert(tk.END, user)
        self.changeImage(self.role)

    def receive_message(self):
        while self.pf:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message and self.start_receiving:
                    if message.split("$")[0] == "PFLOU":
                        print(message)
            except Exception as e:
                print(f"Error : {e}")
                  
    def clickThread(self):
        print("clique")
        with self.lock:
            if self.pfTime > 0:
                self.pf = True
                self.start_receiving =True
                receive_thread = threading.Thread(target = self.receive_message)
                receive_thread.start()
            else:
                self.pf = False

        while self.pf:
            with self.lock:
                self.pfTime -=0.1
                if self.pfTime <= 0:
                    self.client.send("PFEND$Petite fille découverte".encode('utf-8'))
                    self.pf = False
            time.sleep(0.1)
        self.start_receiving = False
        """
        if self.pfTime > 0:
            self.pf = True
            thread = threading.Thread(target = self.receive_message, daemon = True)
            thread.start()
        else:
            self.pf = False
        while self.pf:
            self.pfTime -= 0.1
            time.sleep(0.1)
            if self.pfTime <= 0:
                self.client.send("PFEND$Petite fille découverte".encode("utf-8"))
                self.pf = False
        """
    def pfClick(self, _):
        threading.Thread(target=self.clickThread, daemon=True).start()

    def pfRelease(self, _):
        with self.lock:
            self.pf = False
        print(f"Clique relâché, il reste {round(self.pfTime, 2)} secondes.")
    
    def pfTurn(self):
         if self.role == "Petite-Fille":
            self.pfTime = PETITE_FILLE_TEMPS
            self.petiteFilleAction.pack()
    
    def pfEnd(self):
         if self.role == "Petite-Fille":
            with self.lock:
                self.pf = False
            self.petiteFilleAction.pack_forget()

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
    

    def sendMessage(self):
        if self.canChat:
            if self.loupChat:
                message = "LOUM$"+self.entryMessage.get()
            else:
                message = "CHAT$" + self.entryMessage.get()
            if message != "":
                self.client.send(message.encode("utf-8"))
                self.entryMessage.delete(0, tk.END)

    def chat(self, joueur, message = ""):
    
        """
        Ajoute un message au chat.

        Input:
            joueur (str): Nom du joueur qui envoie le message (vide pour les messages globaux).
            message (str): Contenu du message. Si vide, prend le contenu de `entryMessage`.
        """
        self.chatHistory.config(state='normal')
        self.chatHistory.insert(tk.END, joueur + " : " + message + "\n")
        self.chatHistory.config(state='disabled')
        

    def chronometre(self, temps, condition = None):
    
        """
        Lance un compte à rebours.

        Args:
            temps (int): Temps en secondes pour le compte à rebours.
            condition (function): Fonction qui retourne True pour arrêter le chronomètre prématurément.
        """
        
        for i in range(temps,0,-1):
            if condition == None or not condition():
                self.chronoGUI.configure(text = str(i))
                time.sleep(1)
            else:
                self.chronoGUI.configure(text = "0")
                return


    def updateList(self, playersAlive):
    
        """
        Met à jour la liste des joueurs affichés, indiquant ceux qui sont morts.

        Input:
            playerAlive (list): Liste des joueurs vivants, chaque joueur ayant un attribut `nom`.
        """
        self.listePlayers.delete(0, self.listePlayers.size())
        for player in self.players:
            if player in playersAlive:
                self.listePlayers.insert(tk.END, player)
            else:
                self.listePlayers.insert(tk.END, player + " (mort)")
    
    def updateRoleAction(self, affectedPlayers, obligation=None):
    
        """
        Met à jour la liste des actions disponibles en fonction des joueurs affectés et du rôle.

        Input:
            affectedPlayers (list): Liste des joueurs concernés par l'action.
        """
        if obligation == None:
            aPlayers = affectedPlayers + ["Ne rien faire"]
        else:
            aPlayers = affectedPlayers
        self.roleAction.delete(0, self.listePlayers.size())
        for player in aPlayers:
            self.roleAction.insert(tk.END, player)

    def action(self, affectedPlayers, oblig = None): 
    
        """
        Réalise une action en fonction du rôle actuel et des joueurs affectés.

        Input:
            affectedPlayers (list): Liste des joueurs concernés par l'action.

        Output:
            str: Nom du joueur sélectionné pour l'action, ou None si aucune action n'a été prise.
        """
         
        self.updateRoleAction(affectedPlayers, oblig)
        self.roleAction.pack()
        self.chronometre(50,self.roleAction.curselection)
        if self.roleAction.curselection():
            player = self.roleAction.get(first=self.roleAction.curselection()[0])
            self.roleAction.pack_forget()
            if player == "Ne rien faire":
                return None
            return player
        self.roleAction.pack_forget()
        return None