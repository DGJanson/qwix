"""
    Class that makes slightly more advanced decisions than the Basicplayer
"""

import math

from .basicPlayer import BasicPlayer

class SMAPlayer(BasicPlayer):

    def __init__(self):
        self.name = "Slightly More Advanced Player"

    def makeMove(self, actionList):
        score = 0.0
        result = actionList[0]
        if result["color"] == "error":
            score = score + actionList[0]["totalAvailable"] / 10.0
        if result["color"] == "pass":
            score = score + 5.0
            score = score + actionList[0]["totalAvailable"] / 10.0
            if actionList[0]["scoreDiff"] >= 0:
                score = score - math.sqrt(actionList[0]["scoreDiff"])
            else:
                score = score + 1.0

        if len(actionList) > 1:
            for i in range(1, len(actionList)):
                action = actionList[i]
                actionScore = 11.0 - action["nrInLine"]
                if action["whiteDice"]:
                    actionScore = actionScore + 0.5
                actionScore = actionScore + abs(7 - action["number"])

                if actionScore > score:
                    score = actionScore
                    result = action

        return result
