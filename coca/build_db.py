#!/usr/bin/env python3

import json
import os.path
from queue import Queue
import sqlite3
import sys
from threading import Thread
from clean_ngrams import ngram_hash

#number of threads to use
NTHREADS = 4
#absolute path to this script
DIR = os.path.dirname(os.path.realpath(__file__))
#paths to graph and ngram files
GRAPH_FILE = os.path.join(DIR, '../Haikuu/cue_targets_mapping.json')
NGRAM_FILE = os.path.join(DIR, 'clean_ngrams.json')

#sql
DB_FILE = os.path.join(DIR, '../Haikuu/haikuu.db')
CREATE_NGRAM_TABLE = """
    CREATE TABLE IF NOT EXISTS `ngram_data` (
        id INTEGER PRIMARY KEY,
        ngram TEXT,
        first TEXT,
        last TEXT
    )
"""
INSERT_TO_NGRAM_TABLE = """INSERT INTO `ngram_data` VALUES (?, ?, ?, ?)"""
CREATE_TABLE = """CREATE TABLE IF NOT EXISTS `{}` (nid INTEGER PRIMARY KEY)"""
INSERT_TO_TABLE = """INSERT INTO `{}` (nid) VALUES (?)"""

#load word graph
try:
    with open(GRAPH_FILE) as fin:
        cues = json.load(fin)
        print(GRAPH_FILE, "loaded!")
except IOError as e:
    print(GRAPH_FILE, "not found -- please generate with `generate_map.sh`")
    sys.exit(1)

#load ngrams
try:
    with open(NGRAM_FILE) as fin:
        ngrams = json.load(fin)
        print(NGRAM_FILE, "loaded!")
except IOError as e:
    print(NGRAM_FILE, "not found -- please generate with `clean_ngrams.sh`")
    sys.exit(1)

#create connection to sqlite database
conn = sqlite3.connect(DB_NAME)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

#create ngram_data table and fill
print('creating `ngram_data` table')
cur.execute(CREATE_NGRAM_TABLE)
for ngram in ngrams:
    h = ngram_hash(ngram)
    ngram.insert(0, h)
cur.executemany(INSERT_TO_NGRAM_TABLE, ngrams)
conn.commit()

#delete word associations
print('matching cues and ngrams')
for k in cues.keys():
    del cues[k][:]
    cues[k] = set()
#map cue word to list of ngram ids
for ngram in ngrams:
    for word in ngram[1].split(' '):
        if word in cues.keys():
            cues[word].add(ngram[0])

#create smaller tables and fill
for word in cues.keys():
    print('working on', word)
    cur.execute(CREATE_TABLE.format(word))
    cur.executemany(INSERT_TO_TABLE.format(word), [(i,) for i in cues[word]])
    conn.commit()
