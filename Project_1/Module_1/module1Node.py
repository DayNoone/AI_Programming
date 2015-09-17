import math
from Project_1.genericAStarNode import AStarNode
from gui import drawBoard, initiate


class Module1Node(AStarNode):
    MOVEMENT_COST = 1

    def __init__(self, parent, g, h, x, y, board, heuristic, ninjaNodeMode):
        self.parent = parent
        self.gValue = g
        self.hValue = h
        self.fValue = self.gValue + self.hValue
        self.kids = []

        """Module 1 attributes"""

        self.board = board
        self.heuristic = heuristic
        self.ninjaNodeMode = ninjaNodeMode
        self.xPos = x
        self.yPos = y
        self.state = self.calculateStateIndex()
        self.goalTuple = board.goalXY

        AStarNode.__init__(self, parent)

    def calculateStateIndex(self):
        return int(str(self.xPos) + "00000" + str(self.yPos))

    def __lt__(self, other):
        return self.fValue < other.fValue

    def __str__(self):
        return "Node: X,Y: " + str(self.xPos) + "," + str(self.yPos) + " F: " + str(self.fValue) + "(" + str(
            self.gValue) + "+" + str(self.hValue) + ")"

    def set_gValue(self, newGValue):
        self.gValue = newGValue
        self.fValue = self.gValue + self.hValue

    def set_hValue(self, newHValue):
        self.hValue = newHValue
        self.fValue = self.gValue + self.hValue

    """Algorithm methods"""


    def checkIfGoalState(self):
        if self.xPos == self.goalTuple[0] and self.yPos == self.goalTuple[1]:
            return True
        else:
            return False

    def calculateHeuristicValue(self):
        xOff = math.fabs(self.goalTuple[0] - self.xPos)
        yOff = math.fabs(self.goalTuple[1] - self.yPos)
        if self.heuristic == 1:
            return (xOff + yOff) * self.MOVEMENT_COST
        elif self.heuristic == 2:
            return math.sqrt(xOff * xOff + yOff * yOff) * self.MOVEMENT_COST
        else:
            return 0

    def calculateGValue(self):
        if self.parent is None:
            return 0
        return self.parent.gValue + self.MOVEMENT_COST

    def generate_all_successors(self):
        newChildPositions = [
            (self.xPos + 1, self.yPos),
            (self.xPos - 1, self.yPos),
            (self.xPos, self.yPos + 1),
            (self.xPos, self.yPos - 1)
        ]
        newChildren = []
        for newChildPosition in newChildPositions:
            if 0 <= newChildPosition[0] < len(self.board.boardMatrix) and 0 <= newChildPosition[1] < len(self.board.boardMatrix):
                if self.board.boardMatrix[newChildPosition[0]][newChildPosition[1]] != '#':
                    if self.parent is not None and self.parent.xPos == newChildPosition[0] and self.parent.yPos == \
                            newChildPosition[1]:
                        continue
                    if self.ninjaNodeMode:
                        newChildren.append(
                            Module1NinjaNode(self, 0, 0, newChildPosition[0], newChildPosition[1], self.board, self.heuristic, self.ninjaNodeMode))
                    else:
                        newChildren.append(
                            Module1Node(self, 0, 0, newChildPosition[0], newChildPosition[1], self.board, self.heuristic, self.ninjaNodeMode))

        return newChildren

    def drawBoard(self, openNodes, closedNodes, False):
        drawBoard(self, self.board.boardMatrix, self.board.startXY, self.board.goalXY, openNodes, closedNodes, False)


class Module1NinjaNode(Module1Node):
    def __lt__(self, other):
        if self.fValue == other.fValue:
            return self.gValue > other.gValue
        return self.fValue < other.fValue

    def __str__(self):
        return "Ninja Node: X,Y: " + str(self.xPos) + "," + str(self.yPos) + " F: " + str(self.fValue) + "(" + str(
            self.gValue) + "+" + str(self.hValue) + ")"
