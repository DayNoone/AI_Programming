class Variable:
    def __init__(self, type, position, initDomain):
        self.type = type
        self.position = position
        self.domain = initDomain
        self.value = None