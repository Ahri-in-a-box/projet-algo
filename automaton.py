from state import CState
from transition import CTransition

class CAutomaton:
    def __init__(self, name, output, path = None):
        self.name = name
        if path is None:
            self.path = "./inputs(tests)/" + name[:self.name.index('.')-1].upper() + "/"
        else:
            self.path = path
        self.symboles = []
        self.currentState = []
        self.defaultStates = []
        self.states = []
        self.table = []
        self.output = output

    def load(self):
        #opening file
        try:
            file = open(self.path + self.name, "r")
        except:
            sys.exit("Can't open/read the file " + self.name + "(" + self.path + self.name + ")")

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

                    #considering epsilon transition as # condition
                    elif t.getCondition() == "#" and t.getStart == cs: #Every epsilon transition leading to a state that isn't current is added to the current states list
                        if cs.index(t.getEnd()) < 0:
                            cs.append(t.getEnd())
                
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
            file = open(self.path + fileName, "r")
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
                tmp["fc"] = True
            else:
                tmp["classe"] = "I"
                tmp["fc"] = False

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
            for j in range(0,tabl.index(t)):
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

            #Overwriting states' next class
            for t in tabl:
                t["_classe_"] = None

            i=1
            for t in tabl:
                #Check for similar states considering its class and transitions' ending states' class
                for j in range(0,tabl.index(t)):
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

                if t["_classe_"] is None:
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
                if t["fc"] and state.isAccepting() is False:
                    state.setFinal(True)
                for s in self.symboles:
                    try:
                        #Finding ending state
                        _state_ = None
                        for st in states:
                            if _state_ is None and st.getName() == t["_" + s + "_"]:
                                _state_ = st

                        #checking transition existence
                        exist = False
                        for ts in transitions:
                            if ts.getStart() == state and ts.getEnd() == _state_ and ts.getCondition() == s:
                                exist = True
                        
                        #creating transition
                        if not exist:
                            transitions.append(CTransition(state, _state_, s))
                    except:
                        s #does nothing but skip

        #renaming states
        for s in states:
            s.setName(len(s.getName())-1)

        self.states = states
        self.table = transitions
            
        return self

    def complete(self):
        incompleteStates = []
        #check for every states if they are complete (they have transition for every symboles)
        for state in self.states:
            sym = self.symboles.copy()
            for t in self.table:
                for s in self.symboles:
                    if t.getCondition() == s and t.getStart() == state:
                        if sym.index(s) >= 0:
                            sym.remove(s)
            #Stores the state and its missing symboles
            if len(sym) > 0:
                incompleteStates.append({ "state":state, "symboles":sym })

        #Create the trash state and missing transitions
        if len(incompleteStates) > 0:
            self.states.append(CState(len(self.states)))
            P = self.states[len(self.states)-1]

            for s in self.symboles:
                self.table.append(CTransition(P, P, s))

            for states in incompleteStates:
                for s in states["symboles"]:
                    self.table.append(CTransition(states["state"], P, s))
        
        return self

    def determine(self):

        return