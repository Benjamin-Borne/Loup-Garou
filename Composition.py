import Role

def createComp(nbPlayers):
    match nbPlayers:
        case 8:
            return [Role.LoupGarou()]*2 + [Role.Voyante()] + [Role.Villageois()]*3 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1
        case 9:
            return [Role.LoupGarou()]*2 + [Role.Voyante()] + [Role.Villageois()]*4 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1
        case 10:
            return [Role.LoupGarou()]*2 + [Role.Voyante()] + [Role.Villageois()]*4 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1  + [Role.Villageois()]*1
        case 11:
            return [Role.LoupGarou()]*2 + [Role.Voyante()] + [Role.Villageois()]*5 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1 + [Role.Sorciere()]*1
        case 12:
            return [Role.LoupGarou()]*3 + [Role.Voyante()] + [Role.Villageois()]*4 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1 + [Role.Voleur()]*1  + [Role.Villageois()]*1
        case 13:
            return [Role.LoupGarou()]*3 + [Role.Voyante()] + [Role.Villageois()]*5 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1 + [Role.Voleur()]*1 + [Role.Sorciere()]*1
        case 14:
            return [Role.LoupGarou()]*3 + [Role.Voyante()] + [Role.Villageois()]*6 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1 + [Role.Voleur()]*1 + [Role.Villageois()]*1
        case 15:
            return [Role.LoupGarou()]*3 + [Role.Voyante()] + [Role.Villageois()]*7 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1 + [Role.Voleur()]*1 + [Role.Sorciere()]*1
        case 16:
            return [Role.LoupGarou()]*3 + [Role.Voyante()] + [Role.Villageois()]*7 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1 + [Role.Voleur()]*1 + [Role.Sorciere()]*1 + [Role.Villageois()]*1
        case 17:
            return [Role.LoupGarou()]*4 + [Role.Voyante()] + [Role.Villageois()]*7 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1 + [Role.Voleur()]*1 + [Role.Sorciere()]*1 + [Role.Villageois()]*1
        case 18:
            return [Role.LoupGarou()]*4 + [Role.Voyante()] + [Role.Villageois()]*8 + [Role.Cupidon()]*1 + [Role.Chasseur()]*1 + [Role.Voleur()]*1 + [Role.Sorciere()]*1 + [Role.Villageois()]*1
        case _:
            return []
            