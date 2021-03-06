# -*- coding: utf-8 -*-

__author__  = 'Sal Aguinaga'
__license__ = "GPL"
__version__ = "0.1.0"
__email__   = "saguinag@nd.edu"

import pprint as pp
import pandas as pd
import numpy as np
import re
import json, time, sys, csv
from HTMLParser import HTMLParser
import sys, os, argparse
import traceback
import time, datetime
import ast
import glob
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
plt.style.use('ggplot')

## http://stackoverflow.com/questions/23531608/how-do-i-save-streaming-tweets-in-json-via-tweepy
## https://www.airpair.com/python/posts/top-mistakes-python-big-data-analytics

def level1_json_proc(in_json_fname=""):
	if not in_json_fname:
		print 'Not a valid filename'
		return
	tweets = pd.DataFrame()
	mozsprint_data = []
	tweet_links = []

	for in_file in glob.glob(in_json_fname+"iso*json"):
		print '-- working with:', in_file, '-'*20
		with open(in_file) as f:
			for j,line in enumerate(f):
				rawtweet=""
				try:
					rawtweet = ast.literal_eval(line.strip('\r\n'))
				except Exception, e:
# 					print "this line"
					try:
						rawtweet = json.loads(line.strip('\r\n'))
					except Exception, e:
						print "!!",str(e)
			
				mozsprint_data.append(rawtweet)
# 		print len(mozsprint_data)
# 		break
	
	# Create the dataframe we will use
	tweets = pd.DataFrame()
	# We want to know when a tweet was sent
	tweets['created_at'] = map(lambda tweet: time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')), mozsprint_data)
	# Who is the tweet owner
	tweets['user'] = map(lambda tweet: tweet['user']['screen_name'], mozsprint_data)
	# How many follower this user has
# 	tweets['user_followers_count'] = map(lambda tweet: tweet['user']['followers_count'], mozsprint_data)
	# What is the tweet's content
	tweets['text'] = map(lambda tweet: tweet['text'].encode('utf-8'), mozsprint_data)
	# Get Hyperlinks lnks = re.findall(r'(https?://\S+)', tt)
# 	tweet_links.append(map(lambda tweet: re.findall(r'(https?://\S+)', tweet['text'].encode('utf-8')), mozsprint_data))
	# If available what is the language the tweet is written in# 
# 	tweets['lang'] = map(lambda tweet: tweet['lang'], mozsprint_data)
# 	# If available, where was the tweet sent from ?
# 	tweets['Location'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, mozsprint_data)
# 	# How many times this tweet was retweeted and favorited
# 	tweets['retweet_count'] = map(lambda tweet: tweet['retweet_count'], mozsprint_data)
# 	tweets['favorite_count'] = map(lambda tweet: tweet['favorite_count'], mozsprint_data)
# 			ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(rtweets['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
# 			df = pd.DataFrame([[rtweets['user']['screen_name']],[ rtweets['text']]], index=ts)
# 			df = pd.to_datetime([rtweets['user']['screen_name'], rtweets['text']], format='%d%b%Y:%H:%M:%S.%f')
	
	# Trim DF omit duplicates
	tweets = tweets.drop_duplicates()
	
	# Get links if in tweet
	tmpar= map(lambda tweet: re.findall(r'(https?://\S+)', tweet), tweets['text'])
	from itertools import chain
	tmps =   list(chain.from_iterable(tmpar))
	
	# Save the trimmed tweet links
	np.savetxt('Results/tweets_hyperlinks.tsv',tmps,fmt="%s", delimiter='\t')
	
		
	df = pd.DataFrame(tweets['created_at'].value_counts(), columns=['number_tweets'])
	df['date'] = df.index
	days = [item.split(" ")[0] for item in df['date'].values]
	df['days'] = days
	grouped_tweets = df[['days', 'number_tweets']].groupby('days')
	tweet_growth = grouped_tweets.sum()
	tweet_growth['days']= tweet_growth.index
	print tweet_growth.head()
	tweet_growth['number_tweets'].to_csv('Results/tweet_countxdate.tsv', sep='\t', header=True)

	if 0:
		tweet_growth.plot(kind='bar')
		plt.savefig('outfig', bb_inches='tight')
# 	print df
	
	return 
	
def get_parser():
	parser = argparse.ArgumentParser(description='procjson')
	parser.add_argument('jsonfile', metavar='JSONFILE', help='Input file.')
	parser.add_argument('--version', action='version', version=__version__)
	return parser
  
def main():
	parser = get_parser()
	args = vars(parser.parse_args())
	
	level1_json_proc(args['jsonfile'])
	
 	if not args['jsonfile']:
 		parser.print_help()
 		os._exit(1)

if __name__=='__main__':
  main()
  print 'Done'
