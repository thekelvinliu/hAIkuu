#!/use/bin/env python

import json
from os import environ
import MySQLdb

#connect to local mysql
db = MySQLdb.connect(host='127.0.0.1',
                     user='root',
                     passwd=environ['MYPASS'])
cur = db.cursor(MySQLdb.cursors.DictCursor)

BASE_INSERT = """INSERT INTO test.word_ngram_map (word, ngram) VALUES {};"""
POD = """("{}", "{}")"""

#load files
with open('./wans/cue_target_pairs.json') as fin:
    data = json.load(fin)
with open('./coca/short.txt') as fin:
    ngrams = json.load(fin)

#be comprehensive
words = set(data.keys())
for k in data.keys():
    for w in data[k]:
        words.add(w)
list(words)
print(len(words))
print(len(ngrams))
ngram_dict = {}
for g in ngrams:
    ngram_dict[g] = set(g.split(' '))

#start inserting
while len(words):
    cw = words.pop()
    print(cw)
    ins_lst = [POD.format(cw, k) for k in ngram_dict.keys()
               if cw in ngram_dict[k]]
    if len(ins_lst) == 0:
        continue
    cur.execute(BASE_INSERT.format(", ".join(ins_lst)))
    db.commit()
