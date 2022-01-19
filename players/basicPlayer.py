"""
Basic implementation of the qwix "ai" player
Inherit from this to create more advanced players
"""

class BasicPlayer:

    def __init__(self):
        # nothing to do here really
        pass

    def makeMove(self, actionList):
        """
        Make a decision on a throw. Only receives possible actions and MUST choose one of the actions

        Args:
            actionList (list): list of available actions in this round

        Returns:
            dict: one of the actions from the received list
        """

        # very simple implementation. Choose the first option (usually error or pass)
        # Then iterate over rest and pick the option:
        # lowest index in list
        # furthest from 7

        toReturn = actionList[0]

        if len(actionList) > 1:
            for i in range(1, len(actionList)):
                if actionList[i]["nrInLine"] < 3:
                    if toReturn["color"] == "error" or toReturn["color"] == "pass":
                        toReturn = actionList[i]
                    elif toReturn["nrInLine"] > actionList[i]["nrInLine"]:
                        toReturn = actionList[i]
                    elif toReturn["nrInLine"] == actionList[i]["nrInLine"]:
                        toRetAbs = abs(7 - toReturn["number"])
                        newAbs = abs(7 - actionList[i]["number"])
                        if newAbs > toRetAbs:
                            toReturn = actionList[i]


        return toReturn
