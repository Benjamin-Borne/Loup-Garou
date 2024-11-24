from tkinter import *
from tkinter import scrolledtext
from PIL import *
from random import randint
import time

def false():
    return False


class mainInterface(Tk):
    def __init__(self, playersList, localPlayer):
        Tk.__init__(self)
        self.local = localPlayer
        self.role = self.local.role
        self.frameChat = Frame(self, bg="#848484", width=400)
        self.chatHistory = scrolledtext.ScrolledText(self.frameChat, wrap=WORD, state='disabled')
        self.entryFrame = Frame(self.frameChat)
        self.entryMessage = Entry(self.entryFrame, width=54)
        self.leftFrame = Frame(self, bg="#3396c7")
        self.framePlayer = Frame(self.leftFrame, width=400, height=600, bg="lightblue")
        self.listePlayers = Listbox(self.framePlayer, height=25, width=40, selectmode="single")
        self.chronoGUI = Label(self.leftFrame, text="Liste des joueurs", font=("Arial", 14), bg="lightblue")
        self.players = [playersList[i].nom for i in range(len(playersList))]

        self.roleActionFrame = Frame(self, bg="#3396c7")
        if self.role == "simple-villageois":
            self.roleAction = Label(self.roleActionFrame, text="PAS D'ACTION", font=("Arial", 14), bg="lightblue")
            self.roleAction.pack()
        else:
            self.roleAction = Listbox(self.roleActionFrame, height=25, width=40, selectmode="single")
            self.roleAction.pack()

        self.frameChat.pack_propagate(False)
        self.frameChat.pack(side=RIGHT, padx=10, pady=10, fill="y")

        self.roleActionFrame.pack(side="right")

        self.title("Loup Garou")
        self.iconbitmap("ressources/loup-garou-dos.ico")
        self.config(background="#3396c7")
        self.minsize(975,650)

        self.chatHistory.pack(expand="yes", fill="both")

        self.entryFrame.pack()
        self.entryMessage.pack(side='left')

        self.sendChat = Button(self.entryFrame, text="Envoyer", width=10)
        self.sendChat.pack(side="right")

        self.leftFrame.pack(side=LEFT)
        self.chronoGUI.pack(side ="top")
        
        self.framePlayer.pack(side="bottom", padx=20)

        labelPlayer = Label(self.framePlayer, text="Liste des joueurs", font=("Arial", 14), bg="lightblue")
        labelPlayer.pack(pady=10)

        self.listePlayers.pack(pady=10)
        
        self.sendVote = Button(self.framePlayer, text="Voter", width=10)
        self.sendVote.pack()

        self.frameRole = Frame(self.leftFrame, bg="#3396c7")
        self.frameRole.pack(side="top", pady=20)
        self.img = Image.open("loup-garou-dos"+".png")
        self.img = self.img.resize((200,200))
        self.img = ImageTk.PhotoImage(self.img,(100,100))
        self.roleImg = Label(self.frameRole, image=self.img, bg ="#3396c7")
        self.roleTxt = Label(self.frameRole, text=None, bg="#3396c7",font=("Arial", 28), fg="white")
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
                self.chatHistory.insert(END, joueur + " : " + message + "\n")
                self.chatHistory.config(state='disabled')
                self.entryMessage.delete(0, END)
            else:
                self.chatHistory.config(state='normal')
                self.chatHistory.insert(END, message + "\n")
                self.chatHistory.config(state='disabled')
                self.entryMessage.delete(0, END)

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
                    self.listePlayers.insert(END, player)
                else:
                    self.listePlayers.insert(END, player + " (mort)")
    
    def updateRoleAction(self, affectedPlayers, roleName):
        if roleName == self.role:
            aPlayers = [affectedPlayers[i].nom for i in range(len(affectedPlayers))]
            self.roleAction.delete(0, self.listePlayers.size())
            for player in aPlayers:
                self.roleAction.insert(END, player)

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


