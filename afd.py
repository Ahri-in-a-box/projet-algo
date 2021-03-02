# exec with python3 ./afd.py

import sys

class CAFD:
    def __init__(self, name):
        self.name = name
        self.filePath = "./inputs(tests)/AFD/" + name + ".txt"
        self.symboles = []
        self.currentState = -1
        self.defaultState = -1
        self.finalState = -1
        self.states = []
        self.table = 0

    def print(self):
        print("Name: " + self.name)
        print("filePath: " + self.filePath)
        print("Symboles: ")
        print(self.symboles)
        print("Current state: " + str(self.currentState))
        print("Final state: " + str(self.finalState))
        print("States: ")
        print(self.states)
        print("Transition table: ")
        print(self.table)

    def load(self):
        try:
            file = open(self.filePath, "r")
        except:
            sys.exit("Can't open/read the file " + self.name + ".txt")

        lines = file.readlines()
        file.close()

        for c in lines[0]:
            self.symboles.append(c)
        self.symboles.remove('\n')

        self.currentState = self.defaultState = int(lines[2])
        self.finalState = int(lines[3])
        self.states.extend(range(0,int(lines[1]),1))

        self.table = [[-1 for x in range(int(len(self.symboles)))] for y in range(int(len(self.states)))]

        for i in range(4,len(lines),1):
            tmp = []
            for c in lines[i]:
                if c != ' ' and c != '\n':
                    tmp.append(c)
            
            self.table[int(tmp[0])][self.symboles.index(tmp[2])] = int(tmp[1])

    def check(self, word):      
        self.currentState = self.defaultState

        for c in word:
            if self.currentState == -1:
                return False
            self.currentState = self.table[self.currentState][self.symboles.index(c)]

        return self.currentState == self.finalState

    def checkList(self, wList):
        for word in wList:
            print(word + " -> " + str(self.check(word)))

    def checkFile(self, fileName):
        try:
            file = open("./inputs(tests)/AFD/" + fileName + ".txt", "r")
        except:
            sys.exit("Can't open/read the file " + fileName + ".txt")

        lines = file.readlines()
        file.close()

        for i in range(len(lines)):
            if lines[i][-1] == '\n':
                lines[i] = lines[i][:-1]

        self.checkList(lines)

    def checkFileList(self, fList):
        for f in fList:
            print("\nFile \"" + f + "\":")
            self.checkFile(f)



afd = CAFD("afd1")
afd.load()
#afd.print()
afd.checkFileList(["mots1","mots2","mots3"])