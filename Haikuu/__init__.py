#!/usr/bin/env python

from __future__ import print_function
import os.path
import sqlite3
from flask import Flask
from flask import g
from flask import render_template
from flask import request
import Haikuu.data

app = Flask(__name__)
DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILE = os.path.join(DIR, 'haikuu.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        db = g._database = conn
    return db

@app.teardown_appcontext
def close_connection(e):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def random_word():
    cur = get_db().cursor()
    return data.generate_random(cur)

@app.route('/<word>')
def specific_word(word):
    cur = get_db().cursor()
    haiku = data.generate(word, cur)
    return haiku if haiku is not None else 'Unable to generate haiku :('

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')
