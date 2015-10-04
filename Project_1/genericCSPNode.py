from Project_1.genericAStarNode import AStarNode


class CSPNode(AStarNode):
    def __init__(self, parent):
        AStarNode.__init__(self, parent)


    def addDomains(self, variables):
        numberOfTotalDomain = 0
        for variableId in variables:
            numberOfTotalDomain += len(variables[variableId].domain)
        return numberOfTotalDomain

    def findSmallestVariable(self, variables, smallestVariable, smallestVariableDomainSize):
        for variableId in variables:
            rowVariable = variables[variableId]
            if 1 < len(rowVariable.domain) < smallestVariableDomainSize:
                smallestVariable = rowVariable
                smallestVariableDomainSize = len(smallestVariable.domain)
        return smallestVariable, smallestVariableDomainSize

    def