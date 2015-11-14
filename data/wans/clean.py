#!/usr/bin/env python3

import json
import os

data = {}
#iterate over all text files and add to data dict
for f in os.listdir('.'):
    if f.endswith('.txt'):
        with open(f) as fin:
            for line in fin.readlines():
                if line[0] == '<':
                    continue
                k, v = line.split(', ')[:2]
                if k == 'a' or v == 'a':
                    continue
                k = k.lower()
                v = v.lower()
                if data.get(k) is None:
                    data[k] = set(v)
                else:
                    data[k].add(v)
#convert set values to lists
for k in data.keys():
    data[k] = list(data[k])
#write file
with open('cue_target_pairs.json', 'w') as fout:
    json.dump(data, fout)

#this written file can be later loaded like this:
# with open('cue_target_pairs.json') as fin:
#     wow = json.load(fin)
