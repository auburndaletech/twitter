#!/usr/bin/env python3

import json
import os
import pprint
import configparser
import time
import tweepy
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

config = configparser.ConfigParser()
config.read(os.path.expanduser('~/.twitter.cfg'))

#mashape_key = config.get('Mashape', 'mashape_key')

consumer_key = config.get('Twitter', 'consumer_key')
consumer_secret = config.get('Twitter', 'consumer_secret')
access_token_key = config.get('Twitter', 'access_token_key')
access_token_secret = config.get('Twitter', 'access_token_secret')

twitter_app_auth = {
    'consumer_key': consumer_key,
    'consumer_secret': consumer_secret,
    'access_token_key': access_token_key,
    'access_token_secret': access_token_secret
}

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

twitter = tweepy.API(auth)

pp = pprint.PrettyPrinter(indent=4)

ids = []


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print("sleep")
            time.sleep(60)

for friend in limit_handled(tweepy.Cursor(twitter.followers).items()):
    pp.pprint(friend._json['screen_name'])
    r.set(friend._json['screen_name'], json.dumps(friend._json))
