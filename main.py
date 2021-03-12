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

class CAutomaton:
    def __init__(self, name, output, t: None):
        self.name = name
        if t is None:
            self.type = name[:self.name.index('.')-1].upper()
        else:
            self.type = t
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

    def save(self):
        #opening file
        try:
            file = open(self.output, "w")
        except:
            sys.exit("Can't open/create the file " + self.output)

        #writing symoles
        for c in self.symboles:
            file.write(c)
        file.write('\n')

        #writing number of states
        file.write(str(len(self.states)) + '\n')

        #writing default states
        for ds in self.defaultStates:
            file.write(str(ds.name) + ' ')
        file.write('\n')

        #writing accepting/final states
        for s in self.states:
            if s.isAccepting():
                file.write(str(s.name)+ ' ')
        file.write('\n')

        #writing transitions
        for t in self.table:
            file.write(str(t.getStart().getName()) + ' ' + str(t.getEnd().getName()) + ' ' + t.getCondition() + '\n')

        #closing file
        file.close()

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

    def minimise(self):
        #Moore algorithm

        #Create transition table
        tabl = []
        for s in self.states:
            #Create line for each state
            tmp = {"state": s}
            if tmp["state"].isAccepting():
                tmp["classe"] = "II"
            else:
                tmp["classe"] = "I"

            #tmp is a dictionary with key state refering to its state, classe refering to its state's class (Accepting or not)

            #Fill dictionary with symboles, the ending state and the class of the ending state
            for t in self.table:
                if t.getStart() == tmp["state"]:
                    condi = t.getCondition()
                    tmp[condi] = t.getEnd()
                    if t.getEnd().isAccepting():
                        tmp["_" + condi + "_"] = "II"
                    else:
                        tmp["_" + condi + "_"] = "I"

            tabl.append(tmp)

        i = 1 #iterator for classes' name

        for t in tabl:
            #Check for similar states considering its class and transitions' ending states' class
            for j in range(0,tabl.index(t) - 1):
                t2 = tabl[j]
                if t2["classe"] == t["classe"]:
                    end = True
                    for s in self.symboles:
                        try:
                            if end and t2["_" + s + "_"] != t["_" + s + "_"]:
                                end = False
                        except:
                            end = False 
                    if end:
                        t["_classe_"] = t2["_classe_"]

            if not t.get("_classe_", False):
                _classe_ = ""
                for ind in range(0,i):
                    _classe_ += "I"
                i+=1
                t["_classe_"] = _classe_
        
        #Check differences between new classes and old classes
        i = True
        for t in tabl:
            if i and t["classe"] != t["_classe_"]:
                i = False

        while not i:
            for t in tabl:
                t["classe"] = t["_classe_"]
                for s in self.symboles:
                    t["_" + s + "_"] = tabl[t[s].getName()]["_classe_"]

            i=1

            for t in tabl:
                #Check for similar states considering its class and transitions' ending states' class
                for j in range(0,tabl.index(t) - 1):
                    t2 = tabl[j]
                    if t2["classe"] == t["classe"]:
                        end = True
                        for s in self.symboles:
                            try:
                                if end and t2["_" + s + "_"] != t["_" + s + "_"]:
                                    end = False
                            except:
                                end = False
                        if end:
                            t["_classe_"] = t2["_classe_"]

                    if not t.get("_classe_", False):
                        _classe_ = ""
                        for ind in range(0,i):
                            _classe_ += "I"
                        i+=1
                        t["_classe_"] = _classe_
            
            i = True
            for t in tabl:
                if i and t["classe"] != t["_classe_"]:
                    i = False

        states = []
        transitions = []

        #Create minimised states
        for t in tabl:
            exist = False
            for s in states:
                if s.getName() == t["classe"]:
                    exist = True

            if not exist:
                states.append(CState(t["classe"]))

        #Create minimised transitions
        for t in tabl:
            state = None
            for s in states:
                if state is None and t["classe"] == s.getName():
                    state = s

            if state is not None:
                for s in self.symboles:
                    try:
                        transitions.append(CTransition(state, t[s], s)) #t[s] should be changed for the new ending state
                    except:
                        s #does nothing but skip

        for s in states:
            print(s.getName())
        print()
        for t in transitions:
            t.print()
            
        return 

    def determine(self):

        return

#Checking if mode is provided
if len(sys.argv) <= 1:
    sys.exit("Not enough arguments to run the script")

#modes: 0 = execute automaton, 1 = minimise automaton, 2 = determine automaton
mode = int(sys.argv[1]) 

#Checking mode
if mode < 0 or mode > 2:
    sys.exit("Invalid mode")

#Setting config with args
if mode == 0:
    if len(sys.argv) < 5:
        sys.exit("Not enough arguments to run the script")
    aut = sys.argv[2]
    inp = sys.argv[3]
    outp = sys.argv[4]
else:
    if len(sys.argv) < 4:
        sys.exit("Not enough arguments to run the script")
    aut = sys.argv[2]
    outp = sys.argv[3]

#creating automaton
if mode == 1:
    automaton = CAutomaton(aut, outp, "Minimisation")
elif mode == 2:
    automaton = CAutomaton(aut, outp, "Determinisation")
else:
    automaton = CAutomaton(aut, outp)

automaton.load()

#Executing automaton
if mode == 0:
    automaton.checkFile(inp)
elif mode == 1:
    automaton.minimise()
    automaton.save()
elif mode == 2:
    automaton.determine()
    automaton.save()