#!/usr/bin/env python

from __future__ import print_function
from os import environ
from flask import Flask
from flask import render_template
from flask import request
import Haikuu.data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/haiku', methods=['GET', 'POST'])
def haiku():
    if request.method == 'POST':
        payload = request.get_json()
        if payload.get('keywords') is not None:
            for word in payload['keywords']:
                haiku = data.generate(word)
                if haiku is not None:
                    return haiku
        else:
            return "Error: try again!"
    return render_template('404.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == '__main__':
    app.run()
