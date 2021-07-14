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
    
    def get_user_last_tweet(self, name):
        user_id = self.api.get_user(name).id
        last_tweet = self.api.user_timeline(user_id=user_id, count=1,
                                            exclude_replies=True, include_rts=False)[0]
        
        return last_tweet
    
    def emotion_of_user(self, user_name):
        user_tweet = self.get_user_last_tweet(user_name).text
        
        tweet_translated = self.translate(user_tweet)
        
        return (user_tweet, tweet_translated, self.get_sentiment(tweet_translated))
    
    def print_results(self, user_name):
        tweet, tweet_translated, emotions= self.emotion_of_user(user_name)
        
        print(f'Tweet from {user_name} analyzed: {tweet}')
        
        compound_score = emotions['compound']
        print(f"Compound score:{compound_score}")
        if compound_score >= 0.05:
            print('The tweet has a positive sentiment')
        elif -0.05 < compound_score < 0.05:
            print('The tweet has a neutral sentiment')
        elif compound_score <= 0.05:
            print('The tweet has a negative sentiment')


bot = SentimentBot(keys.API_KEY, keys.API_SECRET_KEY)
bot.print_results('AriasMarti_')
