__author__ = 'saguinag'+'@'+'nd.edu'
__version__ = "0.1.0"

##
##  spip 'scientific publication impact potential'
##

## TODO: some todo list
#

## VersionLog:
# 0.0.1 Initial commit
# Notes:
# http://scipy.github.io/old-wiki/pages/Cookbook/Matplotlib/Show_colormaps


import argparse,traceback
import time, os, sys,  csv, json
import pandas as pd 
import subprocess
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import string

def hello():
	print '-'*80
	print "SPIP: scientific publication impact potential"
	print '-'*80

def is_keywords_or_doi(query):
	import re 
	pattern = re.compile(r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)\b')
	m=pattern.match(query)
	if m:
		return True
	else:
		return False
def get_title_author_for_doi(query):
	import metapub
	cr = metapub.CrossRef()
	r = cr.query(query)
# 	print [r[0]['fullCitation'].split()[:2]]
	au = r[0]['fullCitation'].split()[:2]
	ti = r[0]['title']
	return ti,au
				 	
def save_given_query(query):
	with open ("./data_collection/saved_queries.txt", 'a') as f:
		f.write(query+'\n')
		
def parse_input_args():
	parser = argparse.ArgumentParser(description='query twitter and output to file')
	parser.add_argument('query', metavar='QUERY', help='Keyword query')
	parser.add_argument('--version', action='version', version=__version__)
	args = vars(parser.parse_args())
	return args
		
def main():
	hello()
	args = parse_input_args()
	save_given_query(args['query'])
	# args['query'] = "10.1016.12.31/nature.S0735-1097(98)2000/12/31/34:7-7" # test query
	# args['query'] = "10.1038/nature16041"
	# args['query'] = 'The role of rapid diagnostics in managing Ebola epidemics' # test query
	kywds_doi = is_keywords_or_doi(args['query'])
	key_wrds = []
	if kywds_doi:
		# get the doi's title
		# else split the query into words and use to query twitter
		print '<< doi >>'
		title,author = get_title_author_for_doi(args['query'])
		tt = str(title)
# 		tt = tt.translate(string.punctuation)
		key_wrds = tt.split()
		[key_wrds.append(x.rstrip(',')) for x in author]
		filt_wds = [str(word) for word in key_wrds if str(word) not in stopwords.words('english')]
		if 0:
			print title, [x.decode('ascii')	for x in author]
			print kywds_doi
	else:
		filt_wds = args['query'].split()
	
	print ' '.join(filt_wds)		

	retrn_bool = subprocess.call([sys.executable, './query_past.py', ' '.join(filt_wds)])
	if retrn_bool:	print ('! Something went wrong ...')
	return 
if __name__ == '__main__':

  main()
  print 'Done.'
  sys.exit(0)
