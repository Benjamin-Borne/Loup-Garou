import Role
import random

def createComp(nbPlayers):
    match nbPlayers:
        case 2:
            return [Role.LoupGarou(), Role.Cupidon()]
        case 8:
            compo = [Role.LoupGarou()]*2 + [Role.Voyante()] + [Role.Villageois()]*3 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1
            return random.shuffle(compo)
        case 9:
            compo = [Role.LoupGarou()]*2 + [Role.Voyante()] + [Role.Villageois()]*4 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1
            return random.shuffle(compo)
        case 10:
            compo = [Role.LoupGarou()]*2 + [Role.Voyante()] + [Role.Villageois()]*4 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1  + [Role.Villageois()]*1
            return random.shuffle(compo)
        case 11:
            compo = [Role.LoupGarou()]*2 + [Role.Voyante()] + [Role.Villageois()]*5 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1 + [Role.Sorciere()]*1
            return random.shuffle(compo)
        case 12:
            compo = [Role.LoupGarou()]*3 + [Role.Voyante()] + [Role.Villageois()]*4 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1 + [Role.Voleur()]*1  + [Role.Villageois()]*1
            return random.shuffle(compo)
        case 13:
            compo = [Role.LoupGarou()]*3 + [Role.Voyante()] + [Role.Villageois()]*5 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1 + [Role.Voleur()]*1 + [Role.Sorciere()]*1
            return random.shuffle(compo)
        case 14:
            compo = [Role.LoupGarou()]*3 + [Role.Voyante()] + [Role.Villageois()]*6 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1 + [Role.Voleur()]*1 + [Role.Villageois()]*1
            random.shuffle(compo)
            return compo
        case 15:
            compo = [Role.LoupGarou()]*3 + [Role.Voyante()] + [Role.Villageois()]*7 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1 + [Role.Voleur()]*1 + [Role.Sorciere()]*1
            random.shuffle(compo)
            return compo
        case 16:
            compo = [Role.LoupGarou()]*3 + [Role.Voyante()] + [Role.Villageois()]*7 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1 + [Role.Voleur()]*1 + [Role.Sorciere()]*1 + [Role.Villageois()]*1
            random.shuffle(compo)
            return compo
        case 17:
            compo = [Role.LoupGarou()]*4 + [Role.Voyante()] + [Role.Villageois()]*7 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1 + [Role.Voleur()]*1 + [Role.Sorciere()]*1 + [Role.Villageois()]*1
            random.shuffle(compo)
            return compo
        case 18:
            compo = [Role.LoupGarou()]*4 + [Role.Voyante()] + [Role.Villageois()]*8 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1 + [Role.Voleur()]*1 + [Role.Sorciere()]*1 + [Role.Villageois()]*1
            random.shuffle(compo)
            return compo
        case _:
            return []
            
