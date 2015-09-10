class Node:
    def __init__(self, parent, g, h, x, y):
        self.parent = parent
        self.status = True
        self.gValue = g
        self.hValue = h
        self.fValue = self.gValue + self.hValue
        self.kids = []
        self.state = None

        self.xPos = x
        self.yPos = y

    def __lt__(self, other):
        return self.fValue < other.fValue

    def __str__(self):
        return "X,Y: " + str(self.xPos) + "," + str(self.yPos) + " F: " + str(self.fValue) + "(" + str(self.gValue) + "+" + str(self.hValue) + ")"

    def set_gValue(self, newGValue):
        self.gValue = newGValue
        self.fValue = self.gValue + self.hValue

    def set_hValue(self, newHValue):
        self.hValue = newHValue
        self.fValue = self.gValue + self.hValue


#board = generateBoard(20, 20, 19, 3, 2, 18, [[5, 5, 10, 10], [1, 2, 4, 1]])

