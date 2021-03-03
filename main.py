# exec with python3 ./afd.py

import sys

class CState:
    def __init__(self, name):
        self.name = name
        self.isFinal = False

    def __lt__(self, other):
        if self.name < other.name:
            return True
        else:
            return False

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

    #The function that return the new state is named 'take' since I had no other idea to name it
    def take(self, currentState, event):
        if self.isValid(currentState,event):
            return self.endState
        else:
            return self.startState

class CAutomaton:
    def __init__(self, name, output):
        self.name = name
        self.type = name[:self.name.index('.')-1].upper()
        self.symboles = []
        self.currentState = []
        self.defaultStates = []
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
        #opening file
        try:
            file = open("./inputs(tests)/" + self.type + "/" + self.name, "r")
        except:
            sys.exit("Can't open/read the file " + self.name)

        #reading and closing file
        lines = file.readlines()
        file.close()

        #setting symboles
        for c in lines[0]:
            self.symboles.append(c)
        self.symboles.remove('\n')

        #creating states
        for i in range(0,int(lines[1]),1):
            self.states.append(CState(i))

        #setting default states
        for i in lines[2]:
            if i != '\n' and i != ' ':
                self.defaultStates.append(self.states[int(i)])

        #setting final/accepting states
        for i in lines[3]:
            if i != '\n' and i != ' ':
                self.states[int(i)].setFinal(True)

        #creating transition table (list of transition)
        for i in range(4,len(lines),1):
            tmp = []
            for c in lines[i]:
                if c != ' ' and c != '\n':
                    tmp.append(c)
            
            self.table.append(CTransition(self.states[int(tmp[0])], self.states[int(tmp[1])], tmp[2]))

    def check(self, word):
        #reseting automaton
        self.currentState = self.defaultStates

        #running automaton
        for c in word:
            #Checking all current states (for Non Deterministic Automatons)
            nextStates = []
            for cs in self.currentState:
                #Checking available transitions for the corresponding event and current state
                transi = []
                for t in self.table:
                    if t.isValid(cs, c):
                        transi.append(t)
                
                if len(transi) > 0:
                    for t in transi:
                        nextStates.append(t.take(cs, c))

            if len(nextStates) == 0:
                return 0

            #Swaping state
            self.currentState = sorted(list(set(nextStates)))

        #Checking final state
        for fs in self.currentState:
            if fs.isAccepting():
                return 1
        
        return 0

    def checkList(self, wList):
        file = open(self.output, "w")
        for word in wList:
            file.write(str(self.check(word)) + '\n')
        file.close()

    def checkFile(self, fileName):
        #Opening file
        try:
            file = open("./inputs(tests)/" + self.type + "/" + fileName, "r")
        except:
            sys.exit("Can't open/create the file " + fileName)

        #reading and closing file
        lines = file.readlines()
        file.close()

        #editing words to remove '\n' at the end
        for i in range(len(lines)):
            if lines[i][-1] == '\n':
                lines[i] = lines[i][:-1]

        self.checkList(lines)


#Checking args
if len(sys.argv) < 5:
    sys.exit("Not enough arguments to run the script")

#Setting config with args
mode = int(sys.argv[1])
aut = sys.argv[2]
inp = sys.argv[3]
outp = sys.argv[4]

#creating automaton
automaton = CAutomaton(aut, outp)
automaton.load()

#Executing automaton
if mode == 0:
    automaton.checkFile(inp)