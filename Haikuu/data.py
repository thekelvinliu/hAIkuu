#!/usr/bin/env python

from __future__ import print_function
import json
import os.path
from random import sample
import sys

PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')

#wans
try:
    with open(os.path.join(PATH, 'wans/cue_target_pairs.json')) as fin:
        wan_graph = json.load(fin)
        print("graph loaded")
except IOError as e:
    print('cue_target_pairs.json not found -- please generate with wan_json.sh')
    sys.exit(1)

#ngrams
try:
    with open(os.path.join(PATH, 'coca/short.txt')) as fin:
        ngrams = [line.split(' ') for line in json.load(fin)]
        print("ngrams loaded")
except IOError as e:
    print('short.txt not found -- please generate with clean_grams.py')
    sys.exit(1)

def wan_walk(seed, steps=3):
    """Returns a word related to the seed word."""
    retval = seed
    while steps > 0:
        word = sample(wan_graph[retval], 1)[0]
        if wan_graph.get(word) is not None:
            retval = word
            steps -= 1
    return retval

def get_associations(seed, size=8):
    """Returns a list of size words related to a seed word."""
    if wan_graph.get(seed) is not None:
        return [wan_walk(seed) for i in range(size)]
    else:
        return None

def get_ngram(word):
    """Returns an ngram which contains the given word."""
    candidates = [" ".join(g) for g in ngrams if word in g]
    return sample(candidates, 1)[0]

def match(seed, words):
    """Returns a haiku given a seed and related words by matching ngrams"""
    haiku = [get_ngram(seed)]
    for word in sample(words, 2):
        haiku.append(get_ngram(word))
    return "/".join(haiku)

def generate(seed):
    """Returns a haiku based on a seed list"""
    words = get_associations(seed)
    return match(seed, words) if words is not None else None
