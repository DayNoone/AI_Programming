class Variable:
    def __init__(self, type, position, initDomain):
        self.type = type
        self.position = position
        self.initDomain = initDomain
        self.value = None

    def setValue(self, value):
        self.value = value