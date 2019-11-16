import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
from elasticsearch import Elasticsearch


class TwitterClient(object): 
            ''' 
            Generic Twitter Class for sentiment analysis. 
            '''
            def __init__(self): 

                # attempt authentication 
                try: 
                    self.auth = tweepy.OAuthHandler("KIC5tWGui7OmtN7dXGN0OhoyH", "DfD9AZ0jgURl5BrG3CSJzDZ8yudcIYcVNCbADSyp3zX2fv3aBU")
                    self.auth.set_access_token("1194257145665146880-Zui8N38nyf2adf3O0CSfXS0WOwWQFU", "kqqIDd6YWz4ekQkwAHseQAjds5KQ2vAGQAzGuDXw1NiTV")
                    # create tweepy API object to fetch tweets 
                    self.api = tweepy.API(self.auth) 
                except: 
                    print("Error: Authentication Failed") 

            def clean_tweet(self, tweet): 
                ''' 
                Utility function to clean tweet text by removing links, special characters 
                using simple regex statements. 
                '''
                return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

            def get_tweet_sentiment(self, tweet): 
                ''' 
                Utility function to classify sentiment of passed tweet 
                using textblob's sentiment method 
                '''
                # create TextBlob object of passed tweet text 
                analysis = TextBlob(self.clean_tweet(tweet)) 
                # set sentiment 
                return analysis.sentiment.polarity

            def get_tweets(self, query, count = 10): 
                ''' 
                Main function to fetch tweets and parse them. 
                '''
                # empty list to store parsed tweets 
                tweets = [] 

                try: 
                    # call twitter api to fetch tweets 
                    fetched_tweets = self.api.search(q = query, count = count) 

                    # parsing tweets one by one 
                    for tweet in fetched_tweets: 
                        # empty dictionary to store required params of a tweet 
                        parsed_tweet = {} 

                        # saving text of tweet 
                        parsed_tweet['text'] = tweet.text 
                        # saving sentiment of tweet 
                        parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
                        
                        parsed_tweet['created_at'] = tweet.created_at

                        # appending parsed tweet to tweets list 
                        if tweet.retweet_count > 0: 
                            # if tweet has retweets, ensure that it is appended only once 
                            if parsed_tweet not in tweets: 
                                tweets.append(parsed_tweet) 
                        else: 
                            tweets.append(parsed_tweet) 

                    # return parsed tweets 
                    return tweets 

                except tweepy.TweepError as e: 
                    # print error (if any) 
                    print("Error : " + str(e)) 

                               
                    
def main(): 
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets 
    date_since = "2019-05-16"
    es = Elasticsearch(['https://dreng:mobi123@elastic.dreng.ch:443'])            

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
    
    yb = ['bsc_yb','BSC_YB','YB','Young_boys','BSC Young Boys','ybforever','ybfans']
    
    for ybtext in yb:
         ybtweets = api.get_tweets(query = ybtext, count = 1000)
           
         for ybtweet in ybtweets:
            for anyspieler in spieler_yb:
                if anyspieler.lower() in ybtweet['text'].lower():
                    for activespieler in spieler:
                        if anyspieler.lower() in activespieler.lower():
                            tweet_dict_new = {
                                "name": activespieler,
                                "senti": ybtweet['sentiment'],
                                "datetime": ybtweet['created_at'],
                                "text": ybtweet['text']         
                                }
                            print (json.dumps(tweet_dict_new,default=str))
                            es.index(index ="twitter",body = tweet_dict_new)

     
    for player in spieler:
            tweets = api.get_tweets(query = player, count = 1000) 
            for tweet1 in tweets:
                tweet_dict = {
                    "name": player,
                    "senti": tweet1['sentiment'],
                    "datetime": tweet1['created_at'],
                    "text": tweet1['text']        
                    }
                print (json.dumps(tweet_dict,default=str))
                es.index(index ="twitter",body = tweet_dict)
                
if __name__ == "__main__": 
    # calling main function 
    main() 