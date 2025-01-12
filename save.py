import csv
import os


def save(players, lovers, maire, nuit):
    deleteSave("save.csv")
    save = open("save.csv", "w", encoding="utf-8")
    writer = csv.writer(save)
    writer.writerow(["Nom", "Role", "Est_Vivant", "Est_Maire", "nuit", "Est_En_Couple"])

    for player in players:
        data = [player.nom, player.role , player.est_vivant , player.nom == maire.nom, nuit]
        if player in lovers:
            data.append(True)
        else:
            data.append(False)

        writer.writerow(data)

    save.close()

def deleteSave(saveFile):
    try: 
        os.remove(saveFile)
        print(f"File '{saveFile}' deleted successfully.")
    except FileNotFoundError: 
        print(f"File '{saveFile}' not found.")
