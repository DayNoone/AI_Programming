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


