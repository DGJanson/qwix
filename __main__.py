import logging

from .game.master import QwixGame

logger = logging.getLogger("qwix")

def setupLogging():
    logging.basicConfig(level = logging.INFO)



if __name__ == "__main__":

    setupLogging()

    game = QwixGame()
    game.playGame()
