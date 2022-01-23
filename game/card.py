import logging

logger = logging.getLogger("qwix")

class Card:

    def calcSingleScore(markedList):

        numberMarked = len(markedList)

        if numberMarked == 0:
            return 0

        lastNumber = markedList[-1] # we know there is at least one

        # check for closed line (bonus score)
        if numberMarked > 6 and (lastNumber == 2 or lastNumber == 12):
            nuberMarked = numberMarked + 1

        total = 0

        for i in range(1, numberMarked + 1): # exclusive, so minus 1
            total = total + i

        return total

    def __init__(self):
        self.available = {}
        self.available["blue"] = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        self.available["green"] = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        self.available["red"] = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.available["yellow"] = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        self.marked = {}
        self.marked["blue"] = []
        self.marked["green"] = []
        self.marked["red"] = []
        self.marked["yellow"] = []

        self.wrongThrows = 0

    def isAvailable(self, color, number):
        """
            Returns the position of the number (or -1 if not found)
            Checks if the final number is allowed
        """
        # if final number, need at least 5 marked before it can be marked
        if (color == "blue" and number == 2 and len(self.marked["blue"]) < 5) or \
            (color == "green" and number == 2 and len(self.marked["green"]) < 5) or \
            (color == "red" and number == 12 and len(self.marked["red"]) < 5) or \
            (color == "yellow" and number == 12 and len(self.marked["yellow"]) < 5):
           return -1

        try:
            return(self.available[color].index(number))
        except ValueError:
            return -1


    def markNumber(self, color, number):
        """
        Remove the number from the set.

        Return true if closed the color, false otherwise
        """
        # edge cases -> pass and error
        if color == "pass": # do nothing
            return False

        if color == "error": # increment wrong throws
            self.wrongThrows = self.wrongThrows + 1
            return False

        if (self.isAvailable(color, number) < 0):
            logger.warning("Marking number that is not available")
            return False

        while self.isAvailable(color, number) >= 0:
            self.available[color] = self.available[color][1:]

        self.marked[color].append(number)

        if len(self.available[color]) <= 0:
            return True
        else:
            return False

    def calcScore(self):
        score = 0
        score = score + Card.calcSingleScore(self.marked["blue"])
        score = score + Card.calcSingleScore(self.marked["green"])
        score = score + Card.calcSingleScore(self.marked["red"])
        score = score + Card.calcSingleScore(self.marked["yellow"])

        score = score - (self.wrongThrows * 5)

        return(score)

    def checkDone(self):
        if self.wrongThrows >= 4:
            return True

        finished = 0
        if len(self.available["blue"]) == 0:
            finished = finished + 1
        if len(self.available["green"]) == 0:
            finished = finished + 1
        if len(self.available["yellow"]) == 0:
            finished = finished + 1
        if len(self.available["red"]) == 0:
            finished = finished + 1

        if finished >= 2:
            return True
        else:
            return False
