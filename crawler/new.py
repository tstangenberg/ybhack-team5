import re 
import tweepy 
import os
import sys
import logging
from tweepy import OAuthHandler 
from textblob import TextBlob 
from elasticsearch import Elasticsearch


 #   username = os.environ['ELASTIC_USER']
 #   password = os.environ['ELASTIC_PASS']

def clean_tweet(tweet): 
              
                return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

def get_tweet_sentiment(tweet): 
              
                # create TextBlob object of passed tweet text 
                analysis = TextBlob(clean_tweet(tweet)) 
                # set sentiment 
                return analysis.sentiment.polarity   

auth = tweepy.OAuthHandler("KIC5tWGui7OmtN7dXGN0OhoyH", "DfD9AZ0jgURl5BrG3CSJzDZ8yudcIYcVNCbADSyp3zX2fv3aBU")
auth.set_access_token("1194257145665146880-Zui8N38nyf2adf3O0CSfXS0WOwWQFU", "kqqIDd6YWz4ekQkwAHseQAjds5KQ2vAGQAzGuDXw1NiTV")
api = tweepy.API(auth)   

class MyStreamListener(tweepy.StreamListener):
        def __init__(self, api):
            self.api = api
            self.me = api.me()

        def on_status(self, tweet):
                   for anyspieler in spieler_yb:
                        if anyspieler.lower() in tweet.text.lower():
                            for activespieler in spieler:
                                if anyspieler.lower() in activespieler.lower():
                                    tweet_dict_new = {
                                        "name": activespieler,
                                        "senti": get_tweet_sentiment(tweet.text),
                                        "datetime": tweet.created_at,
                                        "text": tweet.text        
                                        }
                            print (json.dumps(tweet_dict_new,default=str))
                           # es.index(index ="twitter",body = tweet_dict_new)
        def on_error(self, status):
            logging.error("Error detected")
                               
     
spieler = ['Marco Wölfli','David von Ballmoos','Dario Marzino',
           'Frederik Sörensen','Mohamed Ali Camara','Cédric Zesiger',
           'Nicolas Bürgy','Ulisses Garcia','Saidy Janko','Fabian Lustenberger',
           'Jordan Lotomba','Esteban Petignat','Marvin Spielmann','Vincent Sierro',
           'Miralem Sulejmani','Gianluca Gaudino','Nicolas Moumi Ngamaleu','Christian Fassnacht',
           'Michel Aebischer','Sandro Lauper','Christopher Martins','Roger Assalé','Jean-Pierre Nsame',
           'Felix Mambimbi','Guillaume Hoarau']
    
spieler_yb = ['Marco','Wölfli','David', 'vonBallmoos','Dario', 'Marzino',
           'Frederik', 'Sörensen','Mohamed Ali', 'Camara','Cédric', 'Zesiger',
           'Nicolas' ,'Bürgy','Ulisses', 'Garcia','Saidy', 'Janko','Fabian','Lustenberger',
           'Jordan', 'Lotomba','Esteban','Petignat','Marvin', 'Spielmann','Vincent', 'Sierro',
           'Miralem','Sulejmani','Gianluca', 'Gaudino','Nicolas', 'Moumi' 'Ngamaleu','Christian', 'Fassnacht',
           'Michel', 'Aebischer','Sandro', 'Lauper','Christopher' ,'Martins','Roger' 'Assalé','Jean-Pierre', 'Nsame',
           'Felix' ,'Mambimbi','Guillaume', 'Hoarau']
    
yb = ['bsc_yb','BSC_YB','YB','Young_boys','BSC Young Boys','ybforever','ybfans','fussball','swisssuperleague','football','soccer','futbol']                  
     
                
tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)
stream.filter(track = yb)
