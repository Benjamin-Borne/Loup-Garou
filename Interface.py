import tkinter as tk
from tkinter import scrolledtext
from PIL import ImageTk
from PIL import Image
import time

def false():
    return False


class mainInterface(tk.Tk):
    def __init__(self, playersList, localPlayer):
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
        if self.role == "simple-villageois":
            self.roleAction = tk.Label(self.roleActionFrame, text="PAS D'ACTION", font=("Arial", 14), bg="lightblue")
            self.roleAction.pack()
        else:
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
        self.img = Image.open("ressources/"+role+".png")
        self.img = self.img.resize((200,200))
        self.img = ImageTk.PhotoImage(self.img,(100,100))

        self.roleImg.configure(image=self.img)
        self.roleTxt.configure(text=role)

        self.role = role
    

    def chat(self, joueur, message = ""):
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
        for i in range(temps,0,-1):
            if not condition():
                self.chronoGUI.configure(text = str(i))
                time.sleep(1)
            else:
                self.chronoGUI.configure(text = "0")
                return


    def updateList(self, playerAlive):
            playersAlive = [playerAlive[i].nom for i in range(len(playerAlive))]
            self.listePlayers.delete(0, self.listePlayers.size())
            for player in self.players:
                if player in playersAlive:
                    self.listePlayers.insert(tk.END, player)
                else:
                    self.listePlayers.insert(tk.END, player + " (mort)")
    
    def updateRoleAction(self, affectedPlayers, roleName):
        if roleName == self.role:
            aPlayers = [affectedPlayers[i].nom for i in range(len(affectedPlayers))]
            self.roleAction.delete(0, self.listePlayers.size())
            for player in aPlayers:
                self.roleAction.insert(tk.END, player)

    def action(self, affectedPlayers, roleName):  
        if self.local.role == roleName:
            self.updateRoleAction(affectedPlayers, roleName)
            self.roleAction.pack()
            self.chronometre(10,self.roleAction.curselection)
            if self.roleAction.curselection():
                player = self.roleAction.get(first=self.roleAction.curselection()[0])
                self.roleAction.pack_forget()
                return player
        self.roleAction.pack_forget()
        return None       


