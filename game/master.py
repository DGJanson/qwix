"""
    Class that creates the game and manages the playing
"""
import logging

from .card import Card
from .dice import simulateThrow, getPossibleNumbers
from ..players.basicPlayer import BasicPlayer
from ..players.slightlyMoreAdvancedPlayer import SMAPlayer

logger = logging.getLogger("qwix")

class QwixGame:

    def __init__(self):
        self.roundNumber = 1
        self.activePlayer = 0
        self.gameRunning = True
        self.closedColors = set()
        self.curTopScore = 0

        self.setupPlayers()
        logger.info("Game setup ready")


    def setupPlayers(self):
        self.players = []
        self.players.append((Card(), BasicPlayer()))
        self.players.append((Card(), SMAPlayer()))

    def playFullGame(self):

        while self.gameRunning:
            self.playRound(self.roundNumber, self.activePlayer)

            self.roundNumber += 1
            self.activePlayer += 1
            if self.activePlayer >= len(self.players):
                self.activePlayer = 0
            for plyr in self.players:
                if plyr[0].checkDone():
                    self.gameRunning = False
            if self.roundNumber >= 100:
                self.gameRunning = False

        logger.info("Game finished after {} rounds".format(self.roundNumber))
        for plyr in self.players:
            logger.info("Player {} scored:".format(plyr[1].name))
            logger.info("{}".format(plyr[0]))


    def playRound(self, roundNumber, activePlayer):
        logger.info("Playing round {}".format(roundNumber))
        # get diceThrows
        throws = simulateThrow()
        availableActive = getPossibleNumbers(throws, True, self.closedColors) # this gets all combinations for the active player
        availableOther = getPossibleNumbers(throws, False, self.closedColors) # this gets the combinations of white dice only

        for i in range(0, len(self.players)):
            if i == activePlayer:
                result = self.decideActivePlayer(self.players[i], availableActive)
                if self.players[i][0].markNumber(result["color"], result["number"]):
                    self.closedColors.add(result["color"])
                    logger.info("Closed color {}".format(result["color"]))
                if result["color"] != "error": # if no failed throw, then potentially get another throw
                    availableActive = self.pruneAvailable(availableActive, result)
                    result = self.decideOtherPlayer(self.players[i], availableActive)
                    if self.players[i][0].markNumber(result["color"], result["number"]):
                        self.closedColors.add(result["color"])
                        logger.info("Closed color {}".format(result["color"]))
            else:
                result = self.decideOtherPlayer(self.players[i], availableOther)
                if self.players[i][0].markNumber(result["color"], result["number"]):
                    self.closedColors.add(result["color"])
                    logger.info("Closed color {}".format(result["color"]))

        # calc top score
        self.curTopScore = 0
        for i in range(0, len(self.players)):
            if self.players[i][0].calcScore() > self.curTopScore:
                self.curTopScore = self.players[i][0].calcScore()


    def decideActivePlayer(self, player, available):
        playerCard = player[0]
        optionList = []
        optionList.append(self.createOption("error", 0, False, playerCard))

        for av in available:
            if (playerCard.isAvailable(av[0], av[1])) >= 0:
                optionList.append(self.createOption(av[0], av[1], av[2], playerCard))

        logger.debug(optionList)
        result = player[1].makeMove(optionList)
        logger.info("{} chose: {}".format(player[1].name, result))
        return(result)

    def decideOtherPlayer(self, player, available):
        # generate a list of options
        playerCard = player[0]
        optionList = []
        optionList.append(self.createOption("pass", 0, False, playerCard))

        for av in available:
            if playerCard.isAvailable(av[0], av[1]) >= 0:
                optionList.append(self.createOption(av[0], av[1], av[2], playerCard))

        logger.debug(optionList)
        result = player[1].makeMove(optionList)
        logger.info("{} chose: {}".format(player[1].name, result))
        return(result)

    def createOption(self, color, number, whiteDice, card):
        action = {}
        action["color"] = color
        action["number"] = number
        action["whiteDice"] = whiteDice
        action["nrInLine"] = card.isAvailable(color, number)
        action["scoreDiff"] = self.curTopScore - card.calcScore()
        action["totalAvailable"] = card.nrAvailable()

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
