# Import required libraries/files
import praw
import tweepy
import re
import time
import os

print("********************************")
print("Running")
# Reddit REST API connection initialization
reddit = praw.Reddit(client_id = os.environ['REDDIT_CLIENT_ID'], 
    client_secret = os.environ['REDDIT_CLIENT_SECRET'], 
    user_agent = os.environ['REDDIT_USER_AGENT'], 
    username = os.environ['REDDIT_USERNAME'], 
    password = os.environ['REDDIT_PASSWORD']
)
# Twitter API connection
auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
auth.set_access_token(os.environ['TWITTER_ACCESS_TOKEN'], os.environ['TWITTER_ACCESS_TOKEN_SECRET'])
api = tweepy.API(auth, wait_on_rate_limit = True)

# Intialize variables
errors = 0
copyFrom = os.environ['TWITTER_USERNAME']
postTo = os.environ['REDDIT_SUB']

time.sleep(30)
# Get latest tweet
def get_last_tweet(self):
    try:
        tweet = self.user_timeline(copyFrom,count = 1, tweet_mode = "extended", include_entities = True)[0]
        return tweet
    except:
        return None

# Post to reddit function
def post():
    global postTo
    global errors

    try:
        # If there is a URL in the tweet
        if expanded_url != None:
            subreddit = reddit.subreddit(postTo)
            post = subreddit.submit(title, url = expanded_url)
            print("Posted to " + postTo)
            print("Title: " + title)

        # If there is no URL in the tweet
        else:
            subreddit = reddit.subreddit(postTo)
            post = subreddit.submit(title, selftext = post_text)
            print("Posted to " + postTo)
            print("Title: " + title)

        # Sets post flair to DISCUSSION automatically
        flair_id = '9c53efac-cd94-11e7-8824-0eba7e80ccec'
        post.flair.select(flair_id)

    except praw.exceptions.APIException as e:
        print(e.message)

        if(e.error_type == "RATELIMIT"):
            delay = re.search("(\d+) minutes?", e.message)

            if delay:
                delay_seconds = float(int(delay.group(1)) * 60)
                time.sleep(delay_seconds)
                post()
            else:
                delay = re.search("(\d+) seconds", e.message)
                delay_seconds = float(int(delay.group(1)))
                time.sleep(delay_seconds)
                post()

    except:
        errors = errors + 1
        if (errors > 5):
            print("Crashed")
            exit(1)

# Loop to check for new tweets
lastTweet = 0
while True:
    newTweet = get_last_tweet(api)
    if newTweet == None:
        print("*************************************")
        print("No new Tweet Available")
        continue
    if newTweet.id != lastTweet:
        print("*************************************")
        print("Tweet Available")
        lastTweet = newTweet.id
        
        # Remove URL from title
        title = re.sub(r'http\S+', '', newTweet.full_text)
        
        # Prepare reddit post
        mediaUrl = []

        # If tweet has URL
        if newTweet.entities['urls']!=[]:
            print("*************************************")
            print("Tweet has URL")
            expanded_url = newTweet.entities['urls'][0].get('expanded_url')
            url = newTweet.entities['urls'][0].get('url')

        # If tweet has media
        elif 'media' in newTweet.entities:
            print("*************************************")
            print("Tweet has Media")
            for media in newTweet.extended_entities['media']:
                mediaUrl.append(media['media_url'])

            if len(mediaUrl) == 1:
                expanded_url = mediaUrl
                url = None
            elif len(mediaUrl) > 1:
                post_text = ""
                for item in mediaUrl:
                    post_text += item + "\n\n"
                expanded_url = None
                url = None

        # If tweet is only text
        else:
            print("*************************************")
            print("Tweet has Only Text")
            post_text = ""
            expanded_url = None
            url = None

        # If title would be blank
        if title == url:
            title = "Fortnite Twitter"
        post()
