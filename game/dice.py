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

def getPossibleNumbers(diceThrow, includeColorDice = False, excluded_colors = set()):
    toReturn = []
    whiteResult = diceThrow["white_1"] + diceThrow["white_2"]

    if not "blue" in excluded_colors:
        toReturn.append(("blue", whiteResult, True))
    if not "green" in excluded_colors:
        toReturn.append(("green", whiteResult, True))
    if not "yellow" in excluded_colors:
        toReturn.append(("yellow", whiteResult, True))
    if not "red" in excluded_colors:
        toReturn.append(("red", whiteResult, True))


    if (includeColorDice == True):
        if not "blue" in excluded_colors:
            toReturn.append(("blue", diceThrow["white_1"] + diceThrow["blue"], False))
            toReturn.append(("blue", diceThrow["white_2"] + diceThrow["blue"], False))
        if not "green" in excluded_colors:
            toReturn.append(("green", diceThrow["white_1"] + diceThrow["green"], False))
            toReturn.append(("green", diceThrow["white_2"] + diceThrow["green"], False))
        if not "yellow" in excluded_colors:
            toReturn.append(("yellow", diceThrow["white_1"] + diceThrow["yellow"], False))
            toReturn.append(("yellow", diceThrow["white_2"] + diceThrow["yellow"], False))
        if not "red" in excluded_colors:
            toReturn.append(("red", diceThrow["white_1"] + diceThrow["red"], False))
            toReturn.append(("red", diceThrow["white_2"] + diceThrow["red"], False))

    return(toReturn)
