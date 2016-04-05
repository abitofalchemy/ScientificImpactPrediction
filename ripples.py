#!/Users/saguinag/ToolSet/anaconda/bin/python
__author__ = 'saguinag'+'@'+'nd.edu'
__version__ = "0.1.0"

##
##  hrgm = hyperedge replacement grammars model
##

## TODO: some todo list
#

## VersionLog:
# 0.0.1 Initial commit
#

import argparse,traceback,optparse
import time, tweepy, sys, csv
from LocStrmListener import StdOutListener

def twitter_authentication():
  fileNamePaht = "../.env/keys.tsv"
  keys_dict = dict()
  with open(fileNamePaht, 'r') as f:
    inreader = csv.reader(f,delimiter='\t')
    for row in inreader:
      keys_dict[row[0]] = row[1]

    return keys_dict

def get_parser():
  parser = argparse.ArgumentParser(description='query twitter and output to file')
  parser.add_argument('query', metavar='QUERY',    help='Quoted query')
  parser.add_argument('limcnt', metavar='LIMCNT', type=int, help='limit count')
  parser.add_argument('--version', action='version', version=__version__)
  return parser

class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            print status.text
        except Exception, e:
            print 'Encountered Exception Tweet:', e
            pass
        return True

    def on_error(self, status_code):
        print 'Encountered error with status code:' + repr(status_code)
        return True

    def on_data(self, data):
        if 'in_reply_to_status_id' in data:
            status = tweepy.Status.parse(self.api, json.loads(data))
            if self.on_status(status) is False:
                return True
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return True
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return True
        return True

    def on_timeout(self):
        print 'Timeout...'
        return True


def main():
  parser = get_parser()
  args = vars(parser.parse_args())

  print args
  ## Read my twitter auth keys and tokens
  auth_keys = twitter_authentication()

  CONSUMER_KEY = auth_keys['CONSUMER_KEY']
  CONSUMER_SECRET = auth_keys['CONSUMER_SECRET']
  OAUTH_TOKEN=auth_keys['OAUTH_TOKEN']
  OAUTH_TOKEN_SECRET = auth_keys['OAUTH_TOKEN_SECRET']


  ## OAuth process, using the keys and tokens
  auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

  ## Creation of the actual interface, using authentication
  api = tweepy.API(auth)

  trck = args['query']
  print track.split()
  trck = ['dong wang','cyber physical']

  listen = StdOutListener(api, 'test', args['limcnt'])
  stream = tweepy.Stream(auth = api.auth, listener = listen,timeout=60)

  print "Streaming started..."
  print "Searching for:", trck

  try:
#    stream.filter(track=trck, async=True)
    stream.filter(track=trck, async=True,stall_warnings=True)
  except:
    print "error!"
    stream.disconnect()




#def streaming():
#  ## Read my twitter auth keys and tokens
#  auth_keys = twitter_authentication()
#
#  CONSUMER_KEY = auth_keys['CONSUMER_KEY']
#  CONSUMER_SECRET = auth_keys['CONSUMER_SECRET']
#  OAUTH_TOKEN=auth_keys['OAUTH_TOKEN']
#  OAUTH_TOKEN_SECRET = auth_keys['OAUTH_TOKEN_SECRET']
#
#
#  ## OAuth process, using the keys and tokens
#  auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
#  auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
#
#  ## Creation of the actual interface, using authentication
#  api = tweepy.API(auth)
#
#
#  l = StreamListener()
#  streamer = tweepy.Stream(auth=api.auth, listener=l, timeout=36000000)
#
#  setTerms = ['C++ 17']
#  streamer.filter(follow=None,track = setTerms)


if __name__ == '__main__':
  main()
  sys.exit(0)
