class Variable:
    def __init__(self, id, x, y, initDomain):
        self.id = id
        self.xPos = x
        self.yPos = y
        self.constraints = {}
        self.colorid = None
        self.domain = initDomain

    def __str__(self):
        s = 'ID:' + str(self.id) + ' ColorID:' + str(self.colorid) + ' Domain:' + str(self.domain)
        return s