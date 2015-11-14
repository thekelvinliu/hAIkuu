#!/usr/bin/env python

from __future__ import print_function
import json
import os.path
from random import sample

PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')

with open(os.path.join(PATH, 'wans/cue_target_pairs.json')) as fin:
    wan_graph = json.load(fin)

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
        return [wan_walk(seed) for i in xrange(size)]
    else:
        return None

def generate(lst):
    return 'haiku is here'
