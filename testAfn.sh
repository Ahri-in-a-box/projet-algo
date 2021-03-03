#!/bin/bash

i=1
while [[ $i -ne 6 ]]; do
    python3 main.py 0 afn$i.txt mots$i.txt sortie$i.txt
    ((i++))
done