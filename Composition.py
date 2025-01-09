import Role
import random

def createComp(nbPlayers):
    match nbPlayers:
        case 8:
            compo = [Role.LoupGarou() for _ in range(2)] + [Role.Voyante()] + [Role.Villageois() for _ in range(3)] + [Role.Cupidon()] + [Role.Chasseur()]
            random.shuffle(compo)
            return compo
        case 9:
            compo = [Role.LoupGarou() for _ in range(2)]+ [Role.Voyante()] + [Role.Villageois() for _ in range(4)] + [Role.Cupidon()] + [Role.Chasseur()]
            random.shuffle(compo)
            return compo
        case 10:
            compo = [Role.LoupGarou() for _ in range(2)] + [Role.Voyante()] + [Role.Villageois() for _ in range(4)] + [Role.Cupidon()] + [Role.Chasseur()] + [Role.PetiteFille()]
            random.shuffle(compo)
            return compo
        case 11:
            compo = [Role.LoupGarou() for _ in range(2)] + [Role.Voyante()] + [Role.Villageois() for _ in range(5)] + [Role.Cupidon()] + [Role.Chasseur()] + [Role.Sorciere()]
            random.shuffle(compo)
            return compo
        case 12:
            compo = [Role.LoupGarou() for _ in range(3)] + [Role.Voyante()] + [Role.Villageois() for _ in range(4)] + [Role.Cupidon()] + [Role.Chasseur()] + [Role.Voleur()] + [Role.PetiteFille()]
            random.shuffle(compo)
            return compo
        case 13:
            compo = [Role.LoupGarou() for _ in range(3)] + [Role.Voyante()] + [Role.Villageois() for _ in range(5)] + [Role.Cupidon()] + [Role.Chasseur()] + [Role.Voleur()] + [Role.Sorciere()]
            random.shuffle(compo)
            return compo
        case 14:
            compo = [Role.LoupGarou() for _ in range(3)] + [Role.Voyante()] + [Role.Villageois() for _ in range(7)] + [Role.Cupidon()] + [Role.Chasseur()] + [Role.Voleur()] + [Role.PetiteFille()]
            random.shuffle(compo)
            return compo
        case 15:
            compo = [Role.LoupGarou() for _ in range(3)] + [Role.Voyante()] + [Role.Villageois() for _ in range(7)] + [Role.Cupidon()] + [Role.Chasseur()] + [Role.Voleur()] + [Role.Sorciere()]
            random.shuffle(compo)
            return compo
        case 16:
            compo = [Role.LoupGarou() for _ in range(3)] + [Role.Voyante()] + [Role.Villageois() for _ in range(7)] + [Role.Cupidon()] + [Role.Chasseur()] + [Role.Voleur()] + [Role.Sorciere()] + [Role.PetiteFille()]
            random.shuffle(compo)
            return compo
        case 17:
            compo = [Role.LoupGarou() for _ in range(4)] + [Role.Voyante()] + [Role.Villageois() for _ in range(7)] + [Role.Cupidon()] + [Role.Chasseur()] + [Role.Voleur()] + [Role.Sorciere()] + [Role.PetiteFille()]
            random.shuffle(compo)
            return compo
        case 18:
            compo = [Role.LoupGarou() for _ in range(4)] + [Role.Voyante()] + [Role.Villageois() for _ in range(8)] + [Role.Cupidon()] + [Role.Chasseur()] + [Role.Voleur()] + [Role.Sorciere()] + [Role.PetiteFille()  ]
            random.shuffle(compo)
            return compo
        case _:
            return []
            
