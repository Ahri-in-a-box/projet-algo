#!/bin/bash

i=1
while [[ $i -ne 5 ]]; do
    python3 main.py 2 ./inputs\(tests\)/Determinisation/afn$i.txt afd$i.txt
    ((i++))
done

#testing determinised afn
i=1
while [[ $i -ne 5 ]]; do
    python3 main.py 0 ./inputs\(tests\)/Determinisation/afn$i.txt mots$i.txt sortie$i.txt
    python3 main.py 0 ./afd$i.txt ./inputs\(tests\)/Determinisation/mots$i.txt sortieDet$i.txt
    python3 verif.py sortie$i.txt sortieDet$i.txt afd$i
    ((i++))
done

i=1
while [[ $i -ne 5 ]]; do
    rm afd$i.txt sortieDet$i.txt sortie$i.txt
    ((i++))
done