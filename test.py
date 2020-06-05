import tweepy
import datetime

from keys import keys
from config import config
from pprint import pprint

# Twitter API Connection

auth = tweepy.OAuthHandler(keys['twitter_consumer_key'], keys['twitter_consumer_secret'])
auth.set_access_token(keys['twitter_access_token'], keys['twitter_access_token_secret'])
api = tweepy.API(auth, wait_on_rate_limit = True)

tweet = api.user_timeline('FortniteGame',count = 1, tweet_mode = "extended", include_entities = True)[0]
print(tweet.full_text)

if tweet.entities['urls']!=[]:
    url = tweet.entities['urls'][0].get('url')
else:
    url = None

print(url)