#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DL_DIR=$SCRIPT_DIR/downloads
mkdir -p $DL_DIR
url_base=http://w3.usf.edu/FreeAssociation/AppendixA/Cue_Target_Pairs.
for letters in {A-B,C,D-F,G-K,L-O,P-R,S,T-Z}; do
    if [ ! -e $DL_DIR/$letters.txt ]; then
        echo downloading $letters
        curl -# $url_base$letters | iconv -f ISO-8859-1 -t UTF-8 > $DL_DIR/$letters.txt
    fi
done
echo generating json file:
$SCRIPT_DIR/process_wans.py
echo 'done'
