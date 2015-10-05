import copy
from Project_1.genericCSPNode import CSPNode
from gui import initiate, draw_board
from variable import Variable
from Project_1.genericAStarNode import AStarNode


class Node(CSPNode):
    def __init__(self, variables, parent):
        self.variables = variables
        self.parent = parent
        self.gValue = self.calculateGValue()
        self.hValue = self.calculateHeuristicValue()
        self.fValue = self.gValue + self.hValue
        self.kids = []
        self.state = self.calculateStateIndex()
        CSPNode.__init__(self, parent)

    def calculateStateIndex(self):
        string = "0"
        for variableId in self.variables:
            if self.variables[variableId].colorid is not None:
                string += str(variableId) + str(self.variables[variableId].colorid) + "999"
        return int(string)

    """Algorithm methods"""

    def calculateGValue(self):
        if self.parent is None:
            return 0
        return self.parent.gValue + self.MOVEMENT_COST

    def generate_all_successors(self):
        smallestVariable, smallestVariableDomainSize = self.findSmallestVariable(self.variables)

        successors = []

        for value in smallestVariable.domain:
            variablesCopy = copy.deepcopy(self.variables)
            variable = variablesCopy[smallestVariable.id]
            variable.colorid = value
            variable.domain = [value]
            newNode = Node(variablesCopy, self)
            newNode.revise(variable)

            successors.append(newNode)

        return successors

    def revise(self, variable):
        reviseQueue = [variable]

        while len(reviseQueue) != 0:
            newVariable = reviseQueue.pop(0)
            for neighborID in newVariable.constraints[newVariable.id]:
                neighbor = self.variables[neighborID]
                if newVariable.colorid in neighbor.domain:
                    neighbor.domain.remove(newVariable.colorid)
                if len(neighbor.domain) == 1 and neighbor.colorid is None:
                    neighbor.colorid = neighbor.domain[0]
                    reviseQueue.append(neighbor)


    def drawBoard(self, openNodes, closedNodes, isFinished):
        draw_board(self.variables, isFinished)
