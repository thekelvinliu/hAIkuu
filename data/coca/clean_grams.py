#!/usr/bin/env python3

import json
import os

data = {}
c = 2
for f in os.listdir('.'):
    if f.endswith('.txt'):
        with open(f) as fin:
            for line in fin.readlines():
                lst = line.strip().split('\t')[1:]
                data[" ".join(lst[:c])] = " ".join(lst[c:])
        c += 1

with open('ngram_pos_map.json', 'w') as fout:
    json.dump(data, fout)
