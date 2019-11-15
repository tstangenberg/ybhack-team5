#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys
import datetime
from flask import Flask, render_template
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s %(levelname)-5s: %(message)s")
app = Flask(__name__)

username = os.environ['ELASTIC_USER']
password = os.environ['ELASTIC_PASS']
try:
    es = Elasticsearch("https://elastic.dreng.ch",
                       http_auth=(username, password),
                       scheme="https", port=443)
except Exception:
    es = Elasticsearch("elasticsearch-master.efk:9200")


@app.route("/", methods=['GET'])
def root():
    items = [["Spieler 1", "1 Mio.", "2", "0"],
             ["Spieler 2", "1 Mio.", "2", "2"],
             ["Spieler 3", "1 Mio.", "2", "5"]]
    return render_template("index.jinja", info=es.info(), items=items)


@app.route("/healthz", methods=['GET'])
def healthz():
    return {}, 200


def create_indexes():
    settings = {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "name": {"type": "text"},
                "text": {"type": "text"},
                "datetime": {"type": "date"},
            }
        }
    }
    es.indices.create(index="twitter", ignore=400, body=settings)
    settings = {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "name": {"type": "text"},
                "follower": {"type": "integer"},
                "posts": {"type": "integer"},
                "datetime": {"type": "date"},
            }
        }
    }
    es.indices.create(index="insta", ignore=400, body=settings)


def example_data():
    # Add data
    e1 = { "name":"DanielStrohecker",
           "text": "Challenge to challenge the ...",
           "datetime": datetime.datetime.utcnow() }
    es.index(index='twitter', body=e1)

    # search data

    res1 = es.search(index="twitter", body={"query": {"match_all": {}}})

    res2 = es.search(index="twitter", body={'query': {'match': {'name': 'DanielStrohecker', }}})

    print(res1["hits"]["total"]["value"])
    print(res2)

if __name__ == '__main__':
    create_indexes()
    example_data()
    app.run(debug=False, host='0.0.0.0', threaded=True, use_reloader=True)
