#!/bin/bash

url_base=http://w3.usf.edu/FreeAssociation/AppendixA/Cue_Target_Pairs.
for letters in {A-B,C,D-F,G-K,L-O,P-R,S,T-Z}; do
    curl -o $letters.txt $url_base$letters
done
