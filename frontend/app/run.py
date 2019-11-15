#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import sys
import datetime
from flask import Flask, render_template
from elasticsearch import Elasticsearch

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
    count, array = getPlayerList()
    items = calcFame(array)
    return render_template("index.jinja", info=es.info(), items=items, count=countData())


@app.route("/healthz", methods=['GET'])
def healthz():
    return {}, 200


def calcFame(array):
    dataset = []
    for player in array:
        count = searchPlayer(player["name"])
        fame = int((count+1) * (player["follower"]+1) * (player["posts"]+1) / 10000)
        array = [player["name"], player["follower"], player["posts"], count, fame]
        dataset.append(array)
    return dataset


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
                "name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                "follower": {"type": "integer"},
                "posts": {"type": "integer"},
                "datetime": {"type": "date"},
            }
        }
    }
    es.indices.create(index="insta", ignore=400, body=settings)


def getPlayerList():
    # Example data
    e1 = { "name":"Daniel Strohecker",
           "follower": 78,
           "posts": 23,
           "datetime": datetime.datetime.utcnow() }
    #es.index(index="insta", body=e1)

    # search data
    res = es.search(index="insta", body={"query": {"match_all": {}}})
    count = res["hits"]["total"]["value"]
    dataset = []
    for result in res["hits"]["hits"]:
        array = {"name": result["_source"]["name"], 
                 "follower": result["_source"]["follower"], 
                 "posts": result["_source"]["posts"]}
        print(array)
        dataset.append(array)
    return count, dataset


def searchPlayer(player):
    # Example data
    e1 = { "name":"Daniel Strohecker",
           "text": "Challenge to challenge the ...",
           "datetime": datetime.datetime.utcnow() }
    #es.index(index='twitter', body=e1)

    # search data
    res = es.search(index="twitter", body={'query': {'match': {'name': player }}}, size=10000)

    count = res["hits"]["total"]["value"]
    # dataset = []
    # for result in res["hits"]["hits"]:
    #     array = [result["_source"]["name"], result["_source"]["text"], result["_source"]["datetime"], 0]
    #     print(array)
    #     dataset.append(array)
    return count


def countData():
    res = es.search(index="twitter", body={"query": {"match_all": {}}})
    return res["hits"]["total"]["value"]

if __name__ == '__main__':
    create_indexes()
    app.run(debug=False, host='0.0.0.0', threaded=True, use_reloader=True)
