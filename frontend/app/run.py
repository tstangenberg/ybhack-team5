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
    htmlTable = calcFame(array)
    return render_template("index.jinja", table=htmlTable, 
                                          count=countData())


@app.route("/healthz", methods=['GET'])
def healthz():
    return {}, 200


def calcFame(array):
    dataset = []
    for player in array:
        count = searchPlayer(player["name"])
        fame = int((count+1) * (player["follower"]+1) * (player["posts"]+1) / 10000)
        player["fame"] = fame
        player["count"] = count
        dataset.append(player)
    return createHtmlTable(dataset)


def createHtmlTable(dataset):
    htmlTable='<table class="table table-hover text-center" id="datatable-ybhack">'
    htmlTable+="""
               <thead>
                 <tr>
                   <th>Trend</th>
                   <th>Spieler</th>
                   <th>Follower</th>
                   <th>Posts</th>
                   <th>Tweets</th>
                   <th>Fame</th>
                 </tr>
               </thead>
               <tbody>
               """
    for player in dataset:
        if player["fame"] > 10000: icon = '<span class="label label-success"><i class="icon icon-upward"></i></span>'
        elif player["fame"] > 1000: icon = '<span class="label label-warning"><i class="icon icon-forward"></i></span>'
        else: icon = '<span class="label label-error"><i class="icon icon-downward"></i></span>'
        htmlTable+="""
                   <tr>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                     <td>%s</td>
                   </tr>
                   """ % (icon,
                          player["name"], 
                          player["follower"], 
                          player["posts"], 
                          player["count"], 
                          player["fame"])
    htmlTable += "</tbody></table>"
    return htmlTable


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
    settings = {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                "likes": {"type": "integer"},
                "follower": {"type": "integer"},
            }
        }
    }
    es.indices.create(index="facebook", ignore=400, body=settings)


def getPlayerList():
    # Example data
    e1 = { "name":"Daniel Strohecker",
           "follower": 78,
           "posts": 23,
           "datetime": datetime.datetime.utcnow() }
    #es.index(index="insta", body=e1)

    # search data
    res = es.search(index="insta", body={"query": {"match_all": {}}}, size=50)
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
    return count


def countData():
    res = es.search(index="twitter", body={"query": {"match_all": {}}})
    return res["hits"]["total"]["value"]

if __name__ == '__main__':
    create_indexes()
    app.run(debug=False, host='0.0.0.0', threaded=True, use_reloader=True)
