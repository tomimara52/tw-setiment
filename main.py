import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import tweepy
import keys


class SentimentBot:
    
    def __init__(self, key, secret_key):
        auth =  tweepy.AppAuthHandler(key, secret_key)
        self.api = tweepy.API(auth)
    
    def translate(self, text):
        url = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"
        
        querystring = {"q": text.encode("utf-8"),"langpair": "es|en"}

        headers = {
            'x-rapidapi-key': "1fe44fdc00msh0466f0e4f33b7b0p195ab4jsn7d0ff6ad3990",
            'x-rapidapi-host': "translated-mymemory---translation-memory.p.rapidapi.com"
            }
        
        response = requests.request("GET", url, params=querystring, headers=headers)
        
        return response.json()["responseData"]["translatedText"]
    
    def get_sentiment(self, text):
        analyzer = SentimentIntensityAnalyzer()
        
        return analyzer.polarity_scores(text)
    
    def get_user_tweets(self, name, n_of_tweets):
        user_id = self.api.get_user(name).id
        tweets = self.api.user_timeline(user_id=user_id, count=n_of_tweets,
                                            exclude_replies=True, include_rts=False)
        
        return tweets
    
    def emotion_of_user(self, user_name, n_of_tweets):
        tweets = self.get_user_tweets(user_name, n_of_tweets)
        tweets = [tw.text for tw in tweets]
        
        tweets_translated = [self.translate(tw) for tw in tweets]
        
        tweets_sentiment= [self.get_sentiment(tw) for tw in tweets_translated]
        
        return (tweets, tweets_translated, tweets_sentiment)
    
    def print_results(self, user_name, n_of_tweets=1):
        tweets, tweets_translated, tweets_sentiments= self.emotion_of_user(user_name, n_of_tweets)
        
        compound_scores = []
        
        """
        for tw in tweets_translated:
           print(tw)
        """
        
        print(f'Tweets from {user_name} analyzed:')
        for i, tw in enumerate(tweets):
            compound_score = tweets_sentiments[i]['compound']
            compound_scores.append(compound_score)
            
            print("{:-<65} {}".format(tw, compound_score))
            
        compound_mean = sum(compound_scores)/len(compound_scores)
        print(f"Compound score mean:{compound_mean}")
        if compound_mean >= 0.05:
            print('The tweets have a positive sentiment')
        elif -0.05 < compound_mean < 0.05:
            print('The tweets have a neutral sentiment')
        elif compound_mean <= 0.05:
            print('The tweets have a negative sentiment')


bot = SentimentBot(keys.API_KEY, keys.API_SECRET_KEY)
bot.print_results('AriasMarti_', 10)
