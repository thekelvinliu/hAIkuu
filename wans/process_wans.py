#!/usr/bin/env python3

import json
from os import listdir
import os.path

#full path to dowloads directory
DL_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'downloads')
#full path to output file
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           '../Haikuu/cue_targets_mapping.json')

#eventual 'json' object
data = {}
#iterate over all text files and add to data dict
for f in listdir(DL_DIR):
    with open(os.path.join(DL_DIR, f)) as fin:
        for i, line in enumerate(fin):
            #skip any tags and initial header
            if line[0] == '<' or i < 4:
                continue
            k, v = line.lower().split(', ')[:2]
            #skip short words
            if len(k) == 1 or len(v) == 1:
                continue
            if data.get(k) is None:
                data[k] = set()
            data[k].add(v)
#convert sets into sorted lists
for k in data.keys():
    data[k] = sorted(data[k])
#write file
with open(OUTPUT_FILE, 'w') as fout:
    json.dump(data, fout)
print(OUTPUT_FILE)

#this written file can be later loaded like this:
# with open(OUTPUT_FILE) as fin:
#     wow = json.load(fin)
