# -*- coding: utf-8 -*-

__author__  = 'Sal Aguinaga'
__license__ = "GPL"
__version__ = "0.1.0"
__email__  = "saguinag@nd.edu"

from tweepy import StreamListener, Stream
import pprint as pp
import json, time, sys, csv
from HTMLParser import HTMLParser
import sys, os, argparse
import time, datetime
import pandas as pd

# Notes:
# ---- 
## http://stackoverflow.com/questions/23531608/how-do-i-save-streaming-tweets-in-json-via-tweepy

def twitter_authentication():

  ## authentication
  fileNamePaht = "../.env/keys.tsv"
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
    self.output = open(fprefix + '.json', 'a')
  
  def on_status(self, status):
    status = json.loads(HTMLParser().unescape(status))
    if 'indiana' or 'weather' in status.lower():
        # status.created_at is datetime object and status.text is the tweet's text
        text = '::'.join([str(status.created_at), status.text, status.author.screen_name]) + '\n'
        # f.write(text)

def load_clustered_relevant_users():
  infname = "Results/clustered_relevant_users.tsv"
  with open(infname) as f:
    lines = f.readlines()

  sourc =[]
  for j,l in enumerate(lines):
    l = l.rstrip('\r\n')
    lparts = l.split('\t')
    edgesLst= [p.lstrip('[').rstrip(']') for p in lparts]
    sourc.append(edgesLst[0])
  return sourc

def given_screenname_getfollowers():
  import tweepy
  import json
  import numpy as np
  import shelve

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

  #
  ##  From the tq list of tweets, we get those that interacted
  ##  with these tweets and we get a list of their followers to
  ##  to build a graph that expands:
  ##  (pub) -> tq_tweet -> user -> user_followers_list
  #

  fname = 'datasets/tw_users_list_topic1.txt'
  fname = "Results/clustered_relevant_users.tsv"

  if 0:
    scrn_names_lst=[]
    try:
      scrn_names_lst = np.loadtxt(fname,dtype=str)
    except Exception, e:
      print '----'
      with open (fname) as f:
        lines = f.readlines()
        for l in lines:
          l = l.rstrip('\r\n')
          scrn_names_lst.append([x.lstrip('[').rstrip(']') for x in l.split('\t')])
          #scrn_names_lst.append([x.lstrip('[').rstrip(']') for x in l.split()])

    pp.pprint (scrn_names_lst[:20])
    print '----'
    import itertools
    chain = itertools.chain(*scrn_names_lst)
    ids_list = [x for x in list(chain) if x]

    print ids_list[:5]
  else:
    ids_list = load_clustered_relevant_users()

  ## chk what ids have been resolved
  #    
  if os.path.exists('Results/twtrs_follower_network.tsv') and os.stat("Results/twtrs_follower_network.tsv").st_size:
    df = pd.read_csv('Results/twtrs_follower_network.tsv', sep='\t',header=None )

  # 
  usr_followers_d = {}
  outTsv = open("Results/twtrs_follower_network.tsv", "a")
  
  for j,id4usr in enumerate(ids_list):
    id4usr = int(id4usr)
    
    fids = []
    if 'df' in locals() and (id4usr in df[0].values):
      print 'bypassing:', id4usr
      continue

    try:
      for page in tweepy.Cursor(api.followers_ids, id=id4usr).pages():
        fids.extend(page)
        time.sleep(60)
    except Exception, e:
        print '___ error:', e, 'skipping user:', id4usr
        continue

    '''
    # The following code can be accessed if we need str screen_name   
    tuser_ids = [user.screen_name for user in api.lookup_users(user_ids=fids)]
    pp.pprint ([id4usr, tuser_ids])
    if j==4: exit()
    '''
    
    if not(j % 10): print '--<',j,len(fids),'>--'
    usr_followers_d[id4usr] = fids
    outTsv.write("{}\t{}\n".format(id4usr,fids))

  myShelve = shelve.open('Results/tusr_citing_follower_network.shl')
  myShelve['usr_followers_d'] = usr_followers_d
  myShelve.update(usr_followers_d)
  myShelve.close()
  outTsv.close()
  
  # Print # of ids processed
  print 'ids processed:', j

def load_follower_network_tobuild_graph():
  import shelve

  myShelve = shelve.open('tusr_citing_has_follower_network.shl')
  usr_followers_d = myShelve['usr_followers_d']
  myShelve.close()

  print 'Read shelf done'
  for k,v in usr_followers_d.items():
    print k,v
    break


if __name__=='__main__':
  given_screenname_getfollowers()
  #load_follower_network_tobuild_graph()
  print 'Done'
