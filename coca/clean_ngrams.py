#!/usr/bin/env python3

import json
from os import listdir
import os.path

#full path to dowloads directory
DL_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'downloads')
#full path to output file
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           'clean_ngrams.json')

def ngram_hash(ngram_data):
    """returns the hashed value of a piece of ngram data"""
    return hash(''.join(ngram_data))

def main():
    #keep track of seen ngrams
    seen = set()
    #eventual json object
    data = []
    #item to split on
    split = 2
    #iterate over all text files and add to data dict
    for f in listdir(DL_DIR):
        #only process text files
        if not f.endswith('.txt'):
            continue
        print("cleaning", f)
        with open(os.path.join(DL_DIR, f)) as fin:
            for i, line in enumerate(fin):
                lst = line.strip().split('\t')[1:]
                k = " ".join(lst[:split])
                v = lst[split:]
                ngram_data = [k, v[0], v[-1]]
                h = ngram_hash(ngram_data)
                if h not in seen:
                    data.append(ngram_data)
                    seen.add(h)
        split += 1
    #write json file
    with open(OUTPUT_FILE, 'w') as fout:
        json.dump(data, fout)
    print("done", OUTPUT_FILE)

if __name__ == '__main__':
    main()
