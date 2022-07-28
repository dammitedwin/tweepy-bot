import pandas as pd
import tweepy
import configparser
import tweepy
import datetime
import sys
import pytz

utc=pytz.UTC

config = configparser.ConfigParser()
config.read('config.ini')

consumer_key = config['twitter']['consumer_key']
consumer_secret = config['twitter']['consumer_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#sys.argv is the command line arguments
#i.e. python3 tweepyapi.py <- sys.argv[0] "username"<-sys.argv[0]
username = sys.argv[1]
startDate = utc.localize(datetime.datetime(2020, 6, 1, 0, 0, 0))
endDate = utc.localize(datetime.datetime(2020, 1, 1, 0, 0, 0))
tweets = []
tmpTweets = api.user_timeline(username)
for tweet in tmpTweets:
    if tweet.created_at < endDate and tweet.created_at > startDate:
        tweets.append(tweet)

while (tmpTweets[-1].created_at > startDate):
    print("Last Tweet @", tmpTweets[-1].created_at, " - fetching some more")
    tmpTweets = api.user_timeline(username, max_id = tmpTweets[-1].id)
    for tweet in tmpTweets:
        if tweet.created_at < endDate and tweet.created_at > startDate:
            tweets.append(tweet)

df = pd.DataFrame({"tweets":tweet})
df.to_csv(f'{username}',index=False)