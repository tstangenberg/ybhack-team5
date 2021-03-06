#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
import logging
import os
import sys
import datetime
from flask import Flask, render_template
from elasticsearch import Elasticsearch

pp = pprint.PrettyPrinter(indent=4)
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
        result = searchPlayer(player["name"])
        # result ["tweets"]/["likes"]/["follow"] 
        fame = int((result["tweets"]) + 
                   (player["follower"]) + 
                   (player["posts"]) +
                   (result["likes"]) + 
                   (result["follow"]))

        player["follower"] = player["follower"] + result["follow"]
        player["fame"] = fame
        player["tweets"] = result["tweets"]
        player["likes"] = result["likes"]
        dataset.append(player)
    return createHtmlTable(dataset)


def createHtmlTable(dataset):
    sentiList = getSenti()
    htmlTable='<table class="table table-hover text-center" id="datatable-ybhack">'
    htmlTable+="""
               <thead>
                 <tr>
                   <th>Image</th>
                   <th>Spieler</th>
                   <th>Fame</th>
                   <th>Follower</th>
                   <th>Likes</th>
                   <th>Posts</th>
                   <th>Tweets</th>
                 </tr>
               </thead>
               <tbody>
               """
    for player in dataset:
        sentiVal = getPlayerFromSenti(sentiList, player["name"])
        if   sentiVal > 0: 
            icon = '<span class="label label-success"><i class="icon icon-people"></i></span>'
        elif sentiVal == 0: 
            icon = '<span class="label label-warning"><i class="icon icon-people"></i></span>'
        elif sentiVal < 0: 
            icon = '<span class="label label-error"><i class="icon icon-people"></i></span>'
        htmlTable+="""
                   <tr>
                     <td>%s</td>
                     <td>%s</td>
                     <td><b>%s</b></td>
                     <td><img src="static/images/insta.png" width="20" height="20">
                         <img src="static/images/facebook.png" width="20" height="20"> %s</td>
                     <td><img src="static/images/likes.png" width="20" height="20"> %s</td>
                     <td><img src="static/images/insta.png" width="20" height="20"> %s</td>
                     <td><img src="static/images/twitter.png" width="20" height="20"> %s</td>
                   </tr>
                   """ % (icon,
                          player["name"], 
                          player["fame"], 
                          player["follower"], 
                          player["likes"],
                          player["posts"], 
                          player["tweets"])
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
                "name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                "text": {"type": "text"},
                "senti": {"type": "float"},
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
                "follower": {"type": "integer"},
                "posts": {"type": "integer"},
                "datetime": {"type": "date"},
            }
        }
    }
    es.indices.create(index="insta2", ignore=400, body=settings)
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
    res = es.search(index="twitter", body={"query": {"match": {"name": player }}}, size=10000)
    tweets = res["hits"]["total"]["value"]
    res = es.search(index="facebook", body={"query": {"match": {"name": player }}}, size=10000)
    try:
        likes = res["hits"]["hits"][0]["_source"]["likes"]
    except:
        likes = 0
    try:
        follow = res["hits"]["hits"][0]["_source"]["follower"]
    except:
        follow = 0

    return {"tweets": int(tweets), "likes": int(likes), "follow": int(follow)}


def getSenti():
    body = {"size": 1, "aggs": {
              "player_name": {
                "terms": { "field": "name.keyword", "size": 10000 },
                "aggs" : { "avg_senti": { "avg": { "field": "senti" } } }
               }
             }
           }

    res = es.search(index="twitter", body=body, size=1)
    return res["aggregations"]["player_name"]["buckets"]


def getPlayerFromSenti(sentiList, player):
    for entry in sentiList:
        if entry["key"] == player:
            return entry["avg_senti"]["value"]
    return 0


def countData():
    res = es.search(index="twitter", body={"query": {"match_all": {}}})
    return res["hits"]["total"]["value"]


if __name__ == '__main__':
    create_indexes()
    app.run(debug=False, host='0.0.0.0', threaded=True, use_reloader=True)
