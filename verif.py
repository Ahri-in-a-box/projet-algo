import sys

#Checking if mode is provided
if len(sys.argv) <= 3:
    sys.exit("Not enough arguments to run the script")

#Opening provided files
try:
    file1 = open(sys.argv[1], "r")
    file2 = open(sys.argv[2], "r")
except:
    sys.exit("Could not openned one or both provided files")

#Reading files
linesF1 = file1.readlines()
linesF2 = file2.readlines()

#Closing files
file1.close()
file2.close()

#Checking equivalence 
if linesF1 == linesF2:
    print(sys.argv[3] + " has been successfully minimised/determinised!")
else:
    print(sys.argv[3] + " minimisation/determinisation has failed!")

    #Counting errors
    err = 0
    for i in range(0, len(linesF1)):
        if i >= len(linesF2):
            err += len(linesF1) - len(linesF2)
            print(str(err) + " errors found")
            sys.exit()
        if linesF1[i] != linesF2[i]:
            err+=1

    if len(linesF2) > len(linesF1):
        err += len(linesF2) - len(linesF1)

    print(str(err) + " errors found")