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

        self.state = int(str(self.xPos) + "00000" + str(self.yPos))

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


class NinjaNode(Node):
    def __lt__(self, other):
        if self.fValue == other.fValue:
            return self.gValue > other.gValue
        return self.fValue < other.fValue

    def __str__(self):
        return "Ninja Node: X,Y: " + str(self.xPos) + "," + str(self.yPos) + " F: " + str(self.fValue) + "(" + str(
            self.gValue) + "+" + str(self.hValue) + ")"
