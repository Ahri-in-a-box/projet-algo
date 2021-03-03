#!/bin/bash

i=1
while [[ $i -ne 6 ]]; do
    python3 afd.py 0 afd$i.txt mots$i.txt sortie$i.txt
    ((i++))
done