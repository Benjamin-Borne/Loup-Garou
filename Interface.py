from tkinter import *
from tkinter import scrolledtext
from PIL import ImageTk, Image
from random import randint

localPlayer = "Victor"
ROLE = ["loup-garou", "petite-fille","cupidon","chasseur","simple-villageois","voleur","voyante","sorciere"]
currentRole = ROLE[randint(0, len(ROLE)-1)]


window = Tk()

window.title("Loup Garou")
window.iconbitmap("loup-garou-dos.ico")
window.config(background="#3396c7")
window.attributes('-fullscreen', True)

#Interface Chat
def chat():
    message = entryMessage.get()
    if message != "":
        chatHistory.config(state='normal')
        chatHistory.insert(END, localPlayer + " : " + message + "\n")
        chatHistory.config(state='disabled')
        

        entryMessage.delete(0, END)


frameChat = Frame(window, bg="#848484", width=400)
frameChat.pack_propagate(False)
frameChat.pack(side=RIGHT, padx=10, pady=10, fill="y")

chatHistory = scrolledtext.ScrolledText(frameChat, wrap=WORD, state='disabled')
chatHistory.pack(expand="yes", fill="both")

entryFrame = Frame(frameChat)
entryFrame.pack()
entryMessage = Entry(entryFrame, width=54)
entryMessage.pack(side='left')

sendChat = Button(entryFrame, text="Envoyer", width=10, command=chat)
sendChat.pack(side="right")

#Interface joueur
def vote():
    voted = listePlayers.get(first=listePlayers.curselection()[0])
    chatHistory.config(state='normal')
    chatHistory.insert(END, localPlayer + " a voté contre " + voted + "\n")
    chatHistory.config(state='disabled')

    listePlayers.selection_clear(0, END)
    


leftFrame = Frame(window, bg="#3396c7")
leftFrame.pack(side=LEFT)

framePlayer = Frame(leftFrame, width=400, height=600, bg="lightblue")
framePlayer.pack(side="bottom", padx=20)

labelPlayer = Label(framePlayer, text="Liste des joueurs", font=("Arial", 14), bg="lightblue")
labelPlayer.pack(pady=10)

listePlayers = Listbox(framePlayer, height=25, width=40, selectmode="single")

sendVote = Button(framePlayer, text="Voter", width=10, command=vote)
sendVote.pack()

players = [localPlayer, "Joueur 2", "Joueur 3", "Joueur 4", "Joueur 5"]
for player in players:
    listePlayers.insert(END, player)

listePlayers.pack(pady=10)

frameRole = Frame(leftFrame, bg="#3396c7")
frameRole.pack(side="top", pady=20)


img = Image.open(currentRole+".png")
img = img.resize((200,200))
img = ImageTk.PhotoImage(img,(100,100))


roleImg = Label(frameRole, image=img, bg ="#3396c7")
roleImg.pack(side="bottom")
roleTxt = Label(frameRole, text=currentRole, bg="#3396c7",font=("Arial", 28), fg="white")
roleTxt.pack(expand="yes", fill="both", side="top")

window.mainloop()