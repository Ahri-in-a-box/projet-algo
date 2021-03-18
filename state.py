class CState:
    def __init__(self, name):
        self.name = name
        self.isFinal = False

    def __lt__(self, other):
        if self.name < other.name:
            return True
        else:
            return False

    def setName(self, name):
        self.name = name

    def setFinal(self, isFinal):
        self.isFinal = isFinal

    def isAccepting(self):
        return self.isFinal

    def getName(self):
        return self.name