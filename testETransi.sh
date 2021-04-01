#!/bin/bash

#testing eAfn
i=1
while [[ $i -ne 5 ]]; do
    python3 main.py 0 ./inputs\(tests\)/eAFN/eafn$i.txt mots$i.txt sortie$i.txt
    ((i++))
done