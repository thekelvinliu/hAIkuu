#!/usr/bin/env python3

import json
from os import listdir
import os.path

#full path to dowloads directory
DL_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'downloads')
#full path to output file
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           'clean_ngrams.json')

#eventual json object
data = []
#item to split on
split = 2
#iterate over all text files and add to data dict
for f in listdir(DL_DIR):
    print("cleaning", f)
    with open(os.path.join(DL_DIR, f)) as fin:
        for i, line in enumerate(fin):
            lst = line.strip().split('\t')[1:]
            k = " ".join(lst[:split])
            v = lst[split:]
            data.append([k, v[0], v[-1]])
    split += 1

with open(OUTPUT_FILE, 'w') as fout:
    json.dump(data, fout)
print("done", OUTPUT_FILE)
