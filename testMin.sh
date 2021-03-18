#!/bin/bash

i=1
while [[ $i -ne 4 ]]; do
    python3 main.py 1 afd$i.txt afdmin$i.txt
    ((i++))
done

#testing minimised afd
i=1
while [[ $i -ne 4 ]]; do
    python3 main.py 0 ./inputs\(tests\)/Minimisation/afd$i.txt mots$i.txt sortie$i.txt
    python3 main.py 0 ./afdmin$i.txt ./inputs\(tests\)/Minimisation/mots$i.txt sortieMin$i.txt
    python3 verif.py sortie$i.txt sortieMin$i.txt afd$i
    ((i++))
done

i=1
while [[ $i -ne 4 ]]; do
    rm afdmin$i.txt sortieMin$i.txt sortie$i.txt
    ((i++))
done