import sys
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import tweepy
import keys


class SentimentBot:
    
    def __init__(self, key, secret_key):
        auth =  tweepy.AppAuthHandler(key, secret_key)
        self.api = tweepy.API(auth)
        self.translation_keys = [keys.RAPID_API_KEY, keys.RAPID_API_HOST]
    
    def translate(self, text):
        url = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"
        
        querystring = {"q": text.encode("utf-8"),"langpair": "es|en"}

        headers = {
            'x-rapidapi-key': self.translation_keys[0],
            'x-rapidapi-host': self.translation_keys[1]
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
    
    def emotion_of_user(self, user_name, n_of_tweets, is_spanish):
        tweets = self.get_user_tweets(user_name, n_of_tweets)
        tweets = [tw.text for tw in tweets]
        
        tweets_translated = tweets
        if is_spanish:
            tweets_translated = [self.translate(tw) for tw in tweets]
        
        tweets_sentiment= [self.get_sentiment(tw) for tw in tweets_translated]
        
        return (tweets, tweets_translated, tweets_sentiment)
    
    def make_report(self, user_name, n_of_tweets=1, is_spanish=True):
        tweets, _, tweets_sentiments= self.emotion_of_user(user_name, n_of_tweets, is_spanish)
        
        compound_scores = []
        
        """
        for tw in tweets_translated:
           print(tw)
        """
        
        if is_spanish:
            print(f'Tweets de {user_name} analizados:\n')
        else:
            print(f'Tweets from {user_name} analyzed:')
        for i, tw in enumerate(tweets):
            compound_score = tweets_sentiments[i]['compound']
            compound_scores.append(compound_score)
            
            print("{:-<65} {}".format(tw, compound_score))
        print('\n', end='') 
            
        compound_mean = sum(compound_scores)/len(compound_scores)
        
        if is_spanish:
            mean_display_str = f'Media de puntaje compuesto: {compound_mean}'
            sent_display_str = 'Los tweets tienen un sentimiento {}'
            pos = 'positivo'
            neu = 'neutral'
            neg = 'negativo'
        else:
            mean_display_str = f'Compound score mean: {compound_mean}'
            sent_display_str = 'The tweets have a {} sentiment'
            pos = 'positive'
            neu = 'neutral'
            neg = 'negative'
            
        print(mean_display_str)
        if compound_mean >= 0.05:
            print(sent_display_str.format(pos))
        elif -0.05 < compound_mean < 0.05:
            print(sent_display_str.format(neu))
        elif compound_mean <= 0.05:
            print(sent_display_str.format(neg))

if __name__ == '__main__':
    bot = SentimentBot(keys.API_KEY, keys.API_SECRET_KEY)
    args = sys.argv
    
    n_of_tweets = 1
    
    try: 
        user_name = args[1]
    except IndexError as err:
        print('You have to give an user name as argument')
        sys.exit(1)
        
    if len(args) > 2:
        try:
            n_of_tweets = int(args[2])
        except ValueError as err:
            print('The second argument must be an int')
            sys.exit(2)
        
    bot.make_report(user_name, n_of_tweets)
