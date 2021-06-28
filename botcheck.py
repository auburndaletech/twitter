#!/usr/bin/python

import configparser, os
import os, sys
import botometer
import tweepy
import random
import time

config = configparser.ConfigParser()
config.read(os.path.expanduser('~/.twitter.cfg'))

mashape_key = config.get('Mashape', 'mashape_key')

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

bom = botometer.Botometer(wait_on_ratelimit=True,
                          mashape_key=mashape_key,
                          **twitter_app_auth)

fd = open("users.txt")

for userid in fd.readlines():
    userid = userid.rstrip()
    if (not os.path.exists("users/"+userid)):
        print("Writing %s" % (userid))
        result = bom.check_account(userid)
        fd2 = open("users"+userid, "w")
        fd2.write(str(result))
        fd2.close()
        time.sleep(30)
    else:
        print("Skipping %s" % (userid))

