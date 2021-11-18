from random import randint

def simulateThrow():
    toReturn = {}
    toReturn["white_1"] = randint(1,6)
    toReturn["white_2"] = randint(1,6)
    toReturn["blue"] = randint(1,6)
    toReturn["green"] = randint(1,6)
    toReturn["red"] = randint(1,6)
    toReturn["yellow"] = randint(1,6)
    return(toReturn)
    
def getPossibleNumbers(diceThrow, includeColorDice = False):
    toReturn = {}
    whiteResult = diceThrow["white_1"] + diceThrow["white_2"]
    
    toReturn["blue"] = [whiteResult]
    toReturn["green"] = [whiteResult]
    toReturn["red"] = [whiteResult]
    toReturn["yellow"] = [whiteResult]
    
    if (includeColorDice == True):
        toReturn["blue"].append(diceThrow["white_1"] + diceThrow["blue"])
        toReturn["blue"].append(diceThrow["white_2"] + diceThrow["blue"])
        toReturn["green"].append(diceThrow["white_1"] + diceThrow["green"])
        toReturn["green"].append(diceThrow["white_2"] + diceThrow["green"])
        toReturn["red"].append(diceThrow["white_1"] + diceThrow["red"])
        toReturn["red"].append(diceThrow["white_2"] + diceThrow["red"])
        toReturn["yellow"].append(diceThrow["white_1"] + diceThrow["yellow"])
        toReturn["yellow"].append(diceThrow["white_2"] + diceThrow["yellow"])
    
    return(toReturn)
    
    
    