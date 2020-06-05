import tweepy

from keys import keys

def get_tweets(username):
    
    auth = tweepy.OAuthHandler(keys['twitter_consumer_key'], keys['twitter_consumer_secret'])
    auth.set_access_token(keys['twitter_access_token'], keys['twitter_access_token_secret'])

    api = tweepy.API(auth)

    number_of_tweets = 50
    tweets = api.user_timeline(screen_name = username)

    tmp = []
    tweets_for_csv = [tweet.text for tweet in tweets]

    for i in tweets_for_csv:
        tmp.append(i)

    print(tmp)

if __name__ == '__main__':

    get_tweets("FortniteGame")