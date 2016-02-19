#!/usr/bin/env python

from __future__ import print_function
import json
import os.path
import random
import sqlite3
import sys

#absolute path to root Haikuu package
DIR = os.path.dirname(os.path.realpath(__file__))
GRAPH_FILE = 'cue_targets_mapping.json'
BASE_QUERY = """
    SELECT ngram, first, last
    FROM `{0}` as cue
    JOIN `ngram_data` as main
    ON cue.nid = main.id
"""

#load word graph
try:
    with open(os.path.join(DIR, GRAPH_FILE)) as fin:
        word_graph = json.load(fin)
        print(GRAPH_FILE, "loaded!")
except IOError as e:
    print(GRAPH_FILE, "not found -- please generate with `generate_map.sh`")
    sys.exit(1)

def generate_random(cur):
    while True:
        w = random.choice(word_graph.keys())
        h = generate(w, cur)
        if h:
            return ' // '.join([w, h])

def generate(seed, cur):
    """Returns a full haiku based on a seed word."""
    topics = get_associations(seed)
    if topics is None:
        return None
    ngram = get_ngram(seed, cur)
    if ngram is None:
        return None
    ngram.replace("n't", 'not')
    haiku = [ngram]
    i = 2
    while i > 0 and len(topics) > 0:
        random.shuffle(topics)
        ngram = get_ngram(topics.pop(), cur)
        if ngram is not None:
            ngram.replace("n't", 'not')
            haiku.append(ngram)
            i -= 1
    if len(haiku) < 3:
        return None
    else:
        return " / ".join(haiku)

def get_associations(seed, size=8):
    """Returns a list of size words related to a seed word."""
    if word_graph.get(seed) is not None:
        return [random_walk(seed) for i in range(size)]
    else:
        return None

def random_walk(seed, steps=3):
    """Returns related to seed by taking a random walk on the graph"""
    retval = seed
    while steps > 0:
        word = random.choice(word_graph[retval])
        if word_graph.get(word) is not None:
            retval = word
            steps -= 1
    return retval

def get_ngram(word, cur):
    """Returns an ngram containing the given word."""
    cur.execute(BASE_QUERY.format(word))
    res = cur.fetchall()
    return random.choice(res)['ngram'] if res else None
