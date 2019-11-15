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
context = create_default_context(capath="/usr/share/ca-certificates/mozilla")
es = Elasticsearch("https://elastic.dreng.ch",
                   http_auth=(username, password),
                   scheme="https", port=443, ssl_context=context)


@app.route("/", methods=['GET'])
def root():
    items = [["Spieler 1", "1 Mio.", "2", "0"],
             ["Spieler 2", "1 Mio.", "2", "2"],
             ["Spieler 3", "1 Mio.", "2", "5"]]
    return render_template("index.jinja", info=es.info(), items=items)


@app.route("/healthz", methods=['GET'])
def healthz():
    return {}, 200


def create_index(es, index='fame1'):
    settings = {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 0
        },
        "mappings": {
            "members": {
                "dynamic": "strict",
                "properties": {
                    "name": {"type": "text"},
                    "value": {"type": "integer"},
                    "follower": {"type": "integer"},
                    "fame": {"type": "integer"},
                    "source": {"type": "text"},
                }
            }
        }
    }
    try: es.indices.create(index=index_name, ignore=400, body=settings)
    except: pass


if __name__ == '__main__':
    create_index(es)
    app.run(debug=False, host='0.0.0.0', threaded=True, use_reloader=True)
