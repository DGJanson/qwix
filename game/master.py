"""
    Class that creates the game and manages the playing
"""
import logging

from .card import Card
from .dice import simulateThrow, getPossibleNumbers
from ..players.basicPlayer import BasicPlayer

logger = logging.getLogger("qwix")

class QwixGame:

    def __init__(self):
        self.setupPlayers()
        logger.info("Game setup ready")


    def setupPlayers(self):
        self.players = []
        self.players.append((Card(), BasicPlayer()))
        self.players.append((Card(), BasicPlayer()))

    def playGame(self):
        roundNumber = 1
        activePlayer = 0
        gameRunning = True

        while gameRunning: 
            self.playRound(roundNumber, activePlayer)

            roundNumber += 1
            activePlayer += 1
            if activePlayer >= len(self.players):
                activePlayer = 0
            for plyr in self.players:
                if plyr[0].checkDone():
                    gameRunning = False
            if roundNumber >= 100:
                gameRunning = False

        logger.info("Game finished after {} rounds".format(roundNumber))
        for plyr in self.players:
            logger.info("Player scored {} points".format(plyr[0].calcScore()))


    def playRound(self, roundNumber, activePlayer):
        logger.info("Playing round {}".format(roundNumber))
        # get diceThrows
        throws = simulateThrow()
        availableActive = getPossibleNumbers(throws, True) # this gets all combinations for the active player
        availableOther = getPossibleNumbers(throws, False) # this gets the combinations of white dice only

        for i in range(0, len(self.players)):
            if i == activePlayer:
                result = self.decideActivePlayer(self.players[i], availableActive)
                self.players[i][0].markNumber(result["color"], result["number"])
                if result["color"] != "error": # if no failed throw, then potentially get another throw
                    availableActive = self.pruneAvailable(availableActive, result)
                    result = self.decideOtherPlayer(self.players[i], availableActive)
                    self.players[i][0].markNumber(result["color"], result["number"])
            else:
                result = self.decideOtherPlayer(self.players[i], availableOther)
                self.players[i][0].markNumber(result["color"], result["number"])

    def decideActivePlayer(self, player, available):
        optionList = []
        errorAction = {}
        errorAction["color"] = "error"
        errorAction["number"] = 0
        optionList.append(errorAction)

        playerCard = player[0]

        for av in available:
            if (playerCard.isAvailable(av[0], av[1])) >= 0:
                optionList.append(self.createOption(av[0], av[1], av[2], playerCard))

        logger.info(optionList)
        result = player[1].makeMove(optionList)
        logger.info(result)
        return(result)

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
        result = player[1].makeMove(optionList)
        logger.info(result)
        return(result)

    def createOption(self, color, number, whiteDice, card):
        action = {}
        action["color"] = color
        action["number"] = number
        action["whiteDice"] = whiteDice
        action["nrInLine"] = card.isAvailable(color, number)

        return(action)

    def pruneAvailable(self, available, result):
        newAvailable = []

        usedWhiteDice = result["whiteDice"]

        for av in available:
            if usedWhiteDice == False and av[2] == True: # if used color dice, only white options allowed
                if result["color"] != av[0]: # but only if for a different color than the one chosen
                    newAvailable.append(av)
            elif usedWhiteDice == True and av[2] == False: # if used white than all color options are allowed
                 newAvailable.append(av)

        return newAvailable
