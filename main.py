import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import tweepy


class Tw_bot:
    
    def translate(self, text):
        url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

        payload = f"q={text}&target=en&source=es".encode('utf-8')
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'accept-encoding': "application/gzip",
            'x-rapidapi-key': "220056dd15mshb5e219c9e180eb1p1470c8jsnb876b55ffb3f",
            'x-rapidapi-host': "google-translate1.p.rapidapi.com"
            }
        
        response = requests.request("POST", url, data=payload, headers=headers)
        
        return response.text
    
    def get_sentiment(self, text):
        analyzer = SentimentIntensityAnalyzer()
        
        return analyzer.polarity_scores(text)


bot = Tw_bot()
text = bot.translate("harta d estar sola")
print(text)
print(bot.get_sentiment(text))
