# -*- coding: utf-8 -*-

__author__	= 'Sal Aguinaga'
__license__ = "GPL"
__version__ = "0.1.0"
__email__	 =  "saguinag@nd.edu"

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
## http://stackoverflow.com/questions/6500721/find-where-a-t-co-link-goes-to

def level1_json_proc(in_json_fname="", hlinks=False):
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
					try:
						rawtweet = json.loads(line.strip('\r\n'))
					except Exception, e:
						print "!!",str(e)
			
				mozsprint_data.append(rawtweet)

	
	# Create the dataframe we will use
	tweets = pd.DataFrame()
	# We want to know when a tweet was sent
	tweets['created_at'] = map(lambda tweet: time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')), mozsprint_data)
	# Who is the tweet owner
	tweets['user'] = map(lambda tweet: tweet['user']['screen_name'], mozsprint_data)
	tweets['uid'] = map(lambda tweet: tweet['user']['id'], mozsprint_data)
	tweets['docid']= map(lambda tweet: tweet['id'], mozsprint_data)
	# How many follower this user has
  # tweets['user_followers_count'] = map(lambda tweet: tweet['user']['followers_count'], mozsprint_data)
	# What is the tweet's content
	tweets['text'] = map(lambda tweet: tweet['text'].encode('utf-8'), mozsprint_data)
	#print  map(lambda tweet: [tweet['entities']['urls'] for e in tweet.keys() if 'entities' in tweet.keys()], mozsprint_data)
	#tweets['lnks'] = map(lambda tweet: [[h['expanded_url'] for h in tweet[x]['urls'] if 'expanded_url' in h.keys()] for x in tweet.keys() if 'entities' == x], mozsprint_data)
	
	# Trim DF omit duplicates
	tweets = tweets.drop_duplicates()
	
	# Get the extended URLS
	hyperlinks_df = pd.DataFrame()
	hyperlinks_df['docid']= map(lambda tweet: tweet['id'], mozsprint_data)
	hyperlinks_df['xhlnks'] =  map(lambda tweet: [x['expanded_url'] for x in tweet['entities']['urls']] if 'entities' in tweet.keys() else '', mozsprint_data)
	# Get links if in tweet
	hyperlinks_df['text'] = map(lambda tweet: tweet['text'].encode('utf-8'), mozsprint_data)
	hyperlinks_df['hlnksint'] = map(lambda tweet: re.findall(r'(https?://\S+)', tweet), hyperlinks_df['text'])
	
	# print "-- hyperlinks_df"
	# print hyperlinks_df.head()['xhlnks']
	
	print '-'*40
	# tweets['hlinks'] = tweets['text'].apply(lambda t: [t.strip(l) for l in re.findall(r'(https?://\S+)', t) if 'http' in t])
	tweets['cln'] = tweets['text'].apply(lambda t: re.sub(r"http\S+", "", t))

	# Save the trimmed tweet links
	# tweets[['docid','lnks']].to_csv('Results/tweets_cleaned.tsv', sep="\t", index=False, header=False)
	tweets[['uid','docid','cln']].to_csv('Results/tweets_cleaned.tsv', sep="\t", index=False, header=False)
	
	# 	np.savetxt('Results/tweets_hyperlinks.tsv',tmps,fmt="%s", delimiter='\t')
	
	print '-- grouped_tweets'
	# Nbr of tweets on the same date
	df = pd.DataFrame()
	df['number_tweets'] = tweets['created_at'].value_counts()
	df['date'] = df.index
	days = [item.split(" ")[0] for item in df['date'].values]
	df['days'] = days
	grouped_tweets = df[['days', 'number_tweets']].groupby('days').sum()

	# grouped_tweets['days']= grouped_tweets.index
	
	print grouped_tweets.head()
	# tweet_growth['number_tweets'].to_csv('Results/tweet_countxdate.tsv', sep='\t', header=True)

	if 0:
		grouped_tweets.plot(kind='bar')
		plt.savefig('outfig', bb_inches='tight')
	
	return 
	
def get_parser():
	parser = argparse.ArgumentParser(description='procjson_clean clean json files')
	parser.add_argument('jsonfile', metavar='JSONFILE', help='Input Folder')
	parser.add_argument("--do-hyperlinks", default=False, action="store_true" , help='compute metrics and write to disk'+
																							 'example: python procjson_clean.py datasets/ '+
																							 '| Output: Results/tweets_cleaned.tsv')
	parser.add_argument('--version', action='version', version=__version__)
	return parser
	
def main():
	parser = get_parser()
	args = vars(parser.parse_args())
	
	if args['do_hyperlinks']:
		level1_json_proc(args['jsonfile'], hlinks=args['do_hyperlinks'])
	else:
		level1_json_proc(args['jsonfile'])
	
 	if not args['jsonfile']:
 		parser.print_help()
 		os._exit(1)

if __name__=='__main__':
	main()
	print 'Done'
