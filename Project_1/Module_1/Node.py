class Node:
    def __init__(self, parent, g, h, x, y):
        self.parent = parent
        self.status = True
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.kids = []
        self.state = None

        self.x = x
        self.y = y

    def __lt__(self, other):
        return self.f < other.f

    def set_g(self, g):
        self.g = g
        self.f = self.g + self.h
        for kid in self.kids:
            kid.set_g(self.g - 1)


