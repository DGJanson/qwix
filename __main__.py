import logging

from .game.dice import simulateThrow, getPossibleNumbers
from .game.card import Card

logger = logging.getLogger("timeaftertime")

def setupLogging():
    logging.basicConfig(level = logging.INFO)



if __name__ == "__main__":

    setupLogging()
    
    card = Card()
    
    for i in range(0,10):
        throw = getPossibleNumbers(simulateThrow())
        logger.info(throw)
        if (card.isAvailable("blue", throw["blue"][0]) >= 0):
            card.markNumber("blue", throw["blue"][0])
            logger.info("Marked number {}".format(throw["blue"][0]))
            
    logger.info("Score = {}".format(card.calcScore()))
    
    