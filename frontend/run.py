#!/usr/bin/env python
#-*- coding: utf-8 -*-

import logging, sys, os, time
from flask import Flask, jsonify, request, render_template, redirect

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)-5s: %(message)s")
app         = Flask(__name__)


@app.route("/", methods=['GET'])
def root():
    return render_template("index.jinja")

if __name__ == '__main__':
    app.run(debug = False, host = '0.0.0.0', threaded = True, use_reloader = True)

