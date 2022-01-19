"""
    Class that creates the game and manages the playing
"""
import logging

from .card import Card
from .dice import simulateThrow, getPossibleNumbers

logger = logging.getLogger("qwix")

class QwixGame:

    def __init__(self):
        self.setupPlayers()
        logger.info("Game setup ready")


    def setupPlayers(self):
        self.players = []
        self.players.append((Card(), None))
        self.players.append((Card(), None))

    def playGame(self):
        roundNumber = 1
        activePlayer = 0

        for i in range(0,30):
            self.playRound(roundNumber, activePlayer)
            roundNumber += 1
            activePlayer += 1
            if activePlayer >= len(self.players):
                activePlayer = 0

    def playRound(self, roundNumber, activePlayer):
        logger.info("Playing round {}".format(roundNumber))
        # get diceThrows
        throws = simulateThrow()
        availableActive = getPossibleNumbers(throws, True) # this gets all combinations for the active player
        availableOther = getPossibleNumbers(throws, False) # this gets the combinations of white dice only

        for i in range(0, len(self.players)):
            if i == activePlayer:
                result = self.decideActivePlayer(self.players[i], availableActive)
                if result["color"] != "error": # if no failed throw, then potentially get another throw
                    availableActive = self.pruneAvailable(self.players[i], availableActive, result)
                    result = self.decideOtherPlayer(self.players[i], availableActive)
            else:
                result = self.decideOtherPlayer(self.players[i], availableOther)

    def decideActivePlayer(self, player, available):
        optionList = []
        errorAction = {}
        errorAction["color"] = "error"
        errorAction["number"] = 0
        optionList.append(errorAction)

        playerCard = player[0]

        for av in available:
            if (playerCard.isAvailable(av[0], av[1])):
                optionList.append(self.createOption(av[0], av[1], av[2], playerCard))

        logger.info(optionList)

    def decideOtherPlayer(self, player, available):
        # generate a list of options
        optionList = []
        passAction = {}
        passAction["color"] = "pass"
        passAction["number"] = 0
        optionList.append(passAction)

        playerCard = player[0]

        for av in available:
            if playerCard.isAvailable(av[0], av[1]) >= 0:
                optionList.append(self.createOption(av[0], av[1], av[2], playerCard))

        logger.info(optionList)

    def createOption(self, color, number, whiteDice, card):
        action = {}
        action["color"] = color
        action["number"] = number
        action["whiteDice"] = whiteDice
        action["nrInLine"] = card.isAvailable(color, number)

        return(action)

    def pruneAvailable(self, available, result):
        newAvailable = []

        usedColorDice = True
        if result["color"] == "white":
            usedColorDice = False

        for av in available:
            if usedColorDice && av[2] == True: # if used color dice, only white options allowed
                if result["color"] != av[0]: # but only if for a different color than the one chosen
                    newAvailable.push(av)
            elif !usedColorDice && av[2] == False: # if not used color (aka white) than all white options are allowed
                 newAvailable.push(av)

        return newAvailable
