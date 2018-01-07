import tweepy
from credentials import *
from datetime import datetime, timedelta
import _pickle as cPickle
import sys
import logging

logging.basicConfig(filename="tweet_log.log", level=logging.DEBUG)

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
            logging.debug("{} : Successful tweet posting".format(datetime.now()))
        else:
            print('It\'s not bin day today!')

    api = get_api(consumer_key, consumer_secret, access_token, access_token_secret)
    post_tweet(api,"I can post from this bit up here!")
    logging.debug("{} : Successful tweet posting".format(datetime.now()))

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
    api = get_api(consumer_key, consumer_secret, access_token, access_token_secret)
    post_tweet(api,"I can post from my this bit down here!")
    logging.debug("{} : Successful tweet posting".format(datetime.now()))
