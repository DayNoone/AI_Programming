class Variable:
    def __init__(self, rowOrColumn, position, initDomain):
        self.type = rowOrColumn
        self.position = position
        self.domain = initDomain
        self.value = None
