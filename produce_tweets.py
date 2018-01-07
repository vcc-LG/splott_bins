import tweepy
from credentials import *
from datetime import datetime, timedelta
import _pickle as cPickle
import sys

def get_api(consumer_key, consumer_secret, access_token, access_token_secret):
    consumer_secret = consumer_secret.strip('\t')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def post_tweet(api, content):
    api.update_status(content)

def run_produce_tweets():
    try:
        with open('bin_data.p', 'rb') as fp:
            tweet_data = cPickle.load(fp)
    except:
        print("Could not open tweet data")
        sys.exit(1)

    date_now = datetime.now()

    for tweet in tweet_data:
        if tweet['date'].date() - timedelta(days=1) == date_now.date():
            api = get_api(consumer_key, consumer_secret, access_token, access_token_secret)
            post_tweet(api,tweet['text'])
            print('Tweeted about bins!')
        else:
            print('It\'s not bin day today!')

if __name__ == "__main__":
    try:
        with open('bin_data.p', 'rb') as fp:
            tweet_data = cPickle.load(fp)
    except:
        print("Could not open tweet data")
        sys.exit(1)

    date_now = datetime.now()

    for tweet in tweet_data:
        if tweet['date'].date() - timedelta(days=1) == date_now.date():
            api = get_api(consumer_key, consumer_secret, access_token, access_token_secret)
            post_tweet(api,tweet['text'])
            print('Tweeted about bins!')
        else:
            print('It\'s not bin day today!')
