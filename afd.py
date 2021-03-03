# exec with python3 ./afd.py

import sys

class CState:
    def __init__(self, name):
        self.name = name
        self.isFinal = False

    def setFinal(self, isFinal):
        self.isFinal = isFinal

    def isAccepting(self):
        return self.isFinal

    def getName(self):
        return self.name

class CTransition:
    def __init__(self, state1, state2, value):
        self.startState = state1
        self.endState = state2
        self.condition = value

    def print(self):
        print(str(self.startState.getName()) + '-' + str(self.condition) + '->' + str(self.endState.getName()))

    def isValid(self, currentState, event):
        if currentState == self.startState and event == self.condition:
            return True
        else:
            return False

    def take(self, currentState, event):
        if self.isValid(currentState,event):
            return self.endState
        else:
            return self.startState

class CAutomaton:
    def __init__(self, name):
        self.name = name
        self.symboles = []
        self.states = []

class CAFD(CAutomaton):
    def __init__(self, name, output):
        self.name = name
        self.symboles = []
        self.currentState = -1
        self.defaultState = -1
        self.states = []
        self.table = []
        self.output = output

    def print(self):
        print("Name: " + self.name)
        print("Symboles: ")
        print(self.symboles)
        print("Current state: ")
        print(self.currentState)
        print("States: ")
        print(self.states)
        print("Transition table: ")
        print(self.table)

    def load(self):
        try:
            file = open("./inputs(tests)/AFD/" + self.name, "r")
        except:
            sys.exit("Can't open/read the file " + self.name)

        lines = file.readlines()
        file.close()

        for c in lines[0]:
            self.symboles.append(c)
        self.symboles.remove('\n')

        for i in range(0,int(lines[1]),1):
            self.states.append(CState(i))

        for i in lines[3]:
            if i != '\n':
                self.states[int(i)].setFinal(True)

        self.currentState = self.defaultState = self.states[int(lines[2])]

        for i in range(4,len(lines),1):
            tmp = []
            for c in lines[i]:
                if c != ' ' and c != '\n':
                    tmp.append(c)
            
            self.table.append(CTransition(self.states[int(tmp[0])], self.states[int(tmp[1])], tmp[2]))

    def check(self, word):      
        self.currentState = self.defaultState

        for c in word:
            transi = []
            for t in self.table:
                if t.isValid(self.currentState, c):
                    transi.append(t)

            if len(transi) == 0:
                return 0

            self.currentState = transi[0].take(self.currentState, c)

        if self.currentState.isAccepting():
            return 1
        else:
            return 0

    def checkList(self, wList):
        file = open(self.output, "w")
        for word in wList:
            file.write(str(self.check(word)) + '\n')
        file.close()

    def checkFile(self, fileName):
        try:
            file = open("./inputs(tests)/AFD/" + fileName, "r")
        except:
            sys.exit("Can't open/create the file " + fileName)

        lines = file.readlines()
        file.close()

        for i in range(len(lines)):
            if lines[i][-1] == '\n':
                lines[i] = lines[i][:-1]

        self.checkList(lines)

argc = len(sys.argv)

if len(sys.argv) < 5:
    sys.exit("Not enough arguments to run the script")

mode = int(sys.argv[1])
aut = sys.argv[2]
inp = sys.argv[3]
outp = sys.argv[4]

afd = CAFD(aut, outp)
afd.load()

if mode == 0:
    afd.checkFile(inp)