import logging

logger = logging.getLogger("timeaftertime")

class Card:

    def calcSingleScore(numberMarked):
        total = 0
        if numberMarked == 0:
            return 0
        
        for i in range(1, numberMarked + 1):
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
        if (self.isAvailable(color, number) < 0):
            logger.warning("Marking number that is not available")
            return
            
        while self.isAvailable(color, number) >= 0:
            self.available[color] = self.available[color][1:]
        
        self.marked[color].append(number)
    
    def calcScore(self):
        score = 0
        score = score + Card.calcSingleScore(len(self.marked["blue"]))
        score = score + Card.calcSingleScore(len(self.marked["green"]))
        score = score + Card.calcSingleScore(len(self.marked["red"]))
        score = score + Card.calcSingleScore(len(self.marked["yellow"]))
        
        score = score - (self.wrongThrows * 5)
        
        return(score)
        
    