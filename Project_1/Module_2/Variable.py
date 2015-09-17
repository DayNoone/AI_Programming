class Variable:
    def __init__(self, id, x, y):
        self.id = id
        self.xPos = x
        self.yPos = y
        self.neighbor = []
        self.colorid = None