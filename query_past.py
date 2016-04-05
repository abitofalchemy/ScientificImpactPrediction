# -*- coding: utf-8 -*-

__author__  = 'Sal Aguinaga'
__license__ = "GPL"
__version__ = "0.1.0"
__email__   = "saguinag@nd.edu"

from tweepy import StreamListener, Stream
from pprint import pprint
import json, time, sys, csv
from HTMLParser import HTMLParser
import sys, os, argparse
import time, datetime

## http://stackoverflow.com/questions/23531608/how-do-i-save-streaming-tweets-in-json-via-tweepy

def twitter_authentication():

  ## authentication
  fileNamePaht = ".env/keys.tsv"
  keys_dict = dict()
  with open(fileNamePaht, 'r') as f:
    inreader = csv.reader(f,delimiter='\t')
    for row in inreader:
      keys_dict[row[0]] = row[1]

    return keys_dict
#
#follow_acc = ['759251'] #cnn id
#track_words = ['New Zealand flag'] # if remove ReTweets, add '-RT' in the word
# http://stackoverflow.com/questions/32445553/tweepy-not-finding-results-that-should-be-there

class Listener(StreamListener):
  def __init__(self, api = None, fprefix = 'streamer'):
    self.api = api or API()
    self.counter = 0
    self.fprefix = fprefix
    self.output  = open(fprefix + '.json', 'a')
  
  def on_status(self, status):
    status = json.loads(HTMLParser().unescape(status))
    if 'indiana' or 'weather' in stats.lower():
        # status.created_at is datetime object and status.text is the tweet's text
        text = '::'.join([str(status.created_at), status.text, status.author.screen_name]) + '\n'
        f.write(text)


if __name__=='__main__':
 
  import tweepy
  import json

  auth_keys = twitter_authentication()
  CONSUMER_KEY = auth_keys['CONSUMER_KEY']
  CONSUMER_SECRET = auth_keys['CONSUMER_SECRET']
  OAUTH_TOKEN=auth_keys['OAUTH_TOKEN']
  OAUTH_TOKEN_SECRET = auth_keys['OAUTH_TOKEN_SECRET']
  
  # print len (CONSUMER_KEY), len(CONSUMER_SECRET)
  # print len(OAUTH_TOKEN), len(OAUTH_TOKEN_SECRET)
  
  ## OAuth process, using the keys and tokens
  auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
  
  ## Creation of the actual interface, using authentication
  api = tweepy.API(auth)

  # Parse input:
  parser = argparse.ArgumentParser(description='Search Twitter by Query and otuput to file')
  parser.add_argument('query', metavar='QUERY', help='Search Query')
  parser.add_argument('-d', '--verbose', action='store_true', default=False,
                      help='verbose output')

  args = vars(parser.parse_args())
  counter =0
  today = datetime.datetime.today()
  today = today.strftime('%Y-%m-%d')
  print args['query']
  cur = tweepy.Cursor(api.search, \
                      q=args['query'], \
                      since='2015-10-01', until=today).items()
  #cur = tweepy.Cursor(api.search, \
  #        q="Babai AND isomorphism", \
  #        lang="en").items()

  fprefix='Northwind/ScientificImpactPrediction/datasets/' +args['query'].replace(' ','_')+'.json'
  
  # PRINT BLOCK
  print '-'*80
  print 'Given query:', args['query']
  print 'Writing  to:', fprefix
  
  f = open(fprefix, 'a') 
  search_results =[]
  for tweet in cur:
    try:
        print "Tweet created:", tweet.created_at
        print "Tweet:", tweet.text.encode('utf8')
        #twt = json.loads(HTMLParser().unescape(tweet))
        twt = tweet._json 

        f.write(str(twt)+'\n')
        counter += 1

    except IOError:
        time.sleep(60)
        continue

  f.close()
