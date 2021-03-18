import sys

#Checking if mode is provided
if len(sys.argv) <= 3:
    sys.exit("Not enough arguments to run the script")

try:
    file1 = open(sys.argv[1], "r")
    file2 = open(sys.argv[2], "r")

    linesF1 = file1.readlines()
    linesF2 = file2.readlines()

    file1.close()
    file2.close()

    if linesF1 == linesF2:
        print(sys.argv[3] + " has been successfully minimised!")
    else:
        print(sys.argv[3] + " minimisation has failed!")
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
except:
    sys.exit()