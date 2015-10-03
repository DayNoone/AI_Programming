class Variable:
    def __init__(self, type, position, initDomain):
        self.type = type
        self.position = position
        self.domain = initDomain
        self.value = None
        self.id = int(str(9) + str(type) + str(position))

    def setValue(self, value):
        self.value = value