import json
import tweepy
import os

date_since = "2019-10-16"
player_list = ['Marco Wölfli','David von Ballmoos','Dario Marzino',
               'Frederik Sörensen','Mohamed Ali Camara','Cédric Zesiger',
               'Nicolas Bürgy','Ulisses Garcia','Saidy Janko','Fabian Lustenberger',
               'Jordan Lotomba','Esteban Petignat','Marvin Spielmann','Vincent Sierro',
               'Miralem Sulejmani','Gianluca Gaudino','Nicolas Moumi Ngamaleu','Christian Fassnacht',
               'Michel Aebischer','Sandro Lauper','Christopher Martins','Roger Assalé','Jean-Pierre Nsame',
               'Felix Mambimbi','Guillaume Hoarau']
from elasticsearch import Elasticsearch

username = os.environ['ELASTIC_USER']
password = os.environ['ELASTIC_PASS']
try:
    es = Elasticsearch("https://elastic.dreng.ch",
                       http_auth=(username, password),
                       scheme="https", port=443)
except Exception:
    print("using kubernetes service connection to elastic!")
    es = Elasticsearch("elasticsearch-master.efk:9200")


def tweet_to_elastic(tweet, searchterm):
    tweet_dict = {
        "name": searchterm,
        "timestamp": tweet.created_at,
        "text": tweet.text,
        "senti": "unknown"        
    }
    print(tweet_dict)
    es.index(index="twitter", body=tweet_dict)


# Authenticate to Twitter
auth = tweepy.OAuthHandler("KIC5tWGui7OmtN7dXGN0OhoyH", "DfD9AZ0jgURl5BrG3CSJzDZ8yudcIYcVNCbADSyp3zX2fv3aBU")
auth.set_access_token("1194257145665146880-Zui8N38nyf2adf3O0CSfXS0WOwWQFU", "kqqIDd6YWz4ekQkwAHseQAjds5KQ2vAGQAzGuDXw1NiTV")
api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
            for player in player_list:
                if player in tweet.text:
                    tweet_to_elastic(tweet, player)
                
    def on_error(self, status):
        print("Error detected")


tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)
stream.filter(track = player_list)
