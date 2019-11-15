#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys
from flask import Flask, render_template
from elasticsearch import Elasticsearch

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s %(levelname)-5s: %(message)s")
app = Flask(__name__)

username = os.environ['ELASTIC_USER']
password = os.environ['ELASTIC_PASS']
es = Elasticsearch("https://elastic.dreng.ch", 
                    http_auth=(username, password),
                    scheme="https", port=443)


@app.route("/", methods=['GET'])
def root():
    items = [["Spieler 1", "1 Mio.", "2", "0"],
             ["Spieler 2", "1 Mio.", "2", "2"],
             ["Spieler 3", "1 Mio.", "2", "5"]]
    return render_template("index.jinja", info=es.info(), items=items)


@app.route("/healthz", methods=['GET'])
def healthz():
    return {}, 200


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', threaded=True, use_reloader=True)
