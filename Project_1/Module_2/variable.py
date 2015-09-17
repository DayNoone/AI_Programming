class Variable:
    def __init__(self, id, x, y, initDomain):
        self.id = id
        self.xPos = x
        self.yPos = y
        self.neighbor = []
        self.colorid = None
        self.domain = initDomain