class CTransition:
    def __init__(self, state1, state2, value):
        self.startState = state1
        self.endState = state2
        self.condition = value

    def getStart(self):
        return self.startState

    def getEnd(self):
        return self.endState

    def getCondition(self):
        return self.condition

    def isValid(self, currentState, event):
        if currentState == self.startState and event == self.condition:
            return True
        else:
            return False

    #The function that return the new state is named 'take' since I had no other idea to name it
    #Addtionnal note: You can now also use getEnd but it doesn't check if the current state and event validate that transition
    def take(self, currentState, event):
        if self.isValid(currentState,event):
            return self.endState
        else:
            return self.startState
