#!/bin/bash

url_base=http://w3.usf.edu/FreeAssociation/AppendixA/Cue_Target_Pairs.
for letters in {A-B,C,D-F,G-K,L-O,P-R,S,T-Z}; do
    curl $url_base$letters | iconv -f iso-8859-1 -t utf-8 > $letters.txt
done
