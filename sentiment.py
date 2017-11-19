#! /usr/bin/env python

import re
import sqlite3
import sys
import tweepy

from textblob import TextBlob


# Visit https://apps.twitter.com/ 
# login with your account create an
#  app, then paste the following

consumer_key=""
consumer_secret=""
access_key=""
access_secret=""


class CustomStreamListener(tweepy.StreamListener):
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) \
                                    |(\w+:\/\/\S+)", " ", tweet).split())
    def get_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def on_status(self, status):
        ids = status.id_str
        txt = status.text
        sentiment = self.get_sentiment(status.text)
        username = status.user.screen_name
        # we want date & time in unixtime
        created = int(status.created_at.strftime("%s"))
        sqlvalues = [(ids, txt, sentiment, username, created)]
        sql.executemany('INSERT INTO tweets VALUES (?,?,?,?,?)', sqlvalues)
        sqlconnect.commit()

    def on_error(self, status_code):
        print >> sys.stderr, 'Status Code Error :', status_code 
        # Don't kill the stream
        return True

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        # Don't kill the stream
        return True


sqlconnect = sqlite3.connect('sentiment.db')
sql = sqlconnect.cursor()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
api = tweepy.streaming.Stream(auth, CustomStreamListener())

# this includes too many french tweets, changed to custom
# bounding box which has less french tweets
# api.filter(locations=[-3.26,4.63,1.2,11.18])

api.filter(locations=[-3.27,4.46,1.21,11.09])
