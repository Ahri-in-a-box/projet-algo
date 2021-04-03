import sys
from automaton import CAutomaton

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

if aut[0] == '.':
    path = aut[:aut.rindex('/') + 1]
    aut = aut[aut.rindex('/') + 1:]
else:
    path = None
    

#creating automaton
if path:
    automaton = CAutomaton(aut, outp, path)
else:
    automaton = CAutomaton(aut, outp)
automaton.load()

#Executing automaton
if mode == 0:
    automaton.checkFile(inp)
elif mode == 1:
    automaton.complete().minimise().save()
elif mode == 2:
    automaton.determine().save()