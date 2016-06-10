#	-*-	coding:	utf-8	-*-

__author__	=	'Sal	Aguinaga'
__license__	=	"GPL"
__version__	=	"0.1.0"
__email__		=	"saguinag@nd.edu"

import	pprint	as	pp
import	pandas	as	pd
import	numpy	as	np
from	nltk.cluster	import	KMeansClusterer,	GAAClusterer,	euclidean_distance
import	nltk.corpus
import	nltk.stem
import	re
import	io
import	json,	time,	sys,	csv
from	HTMLParser	import	HTMLParser

import	sys,	os,	argparse
import	traceback
import	time,	datetime
import	ast
import	glob
import	matplotlib
matplotlib.use('pdf')
import	matplotlib.pyplot	as	plt
plt.style.use('ggplot')

##	http://stackoverflow.com/questions/23531608/how-do-i-save-streaming-tweets-in-json-via-tweepy
##	https://www.airpair.com/python/posts/top-mistakes-python-big-data-analytics
##	Gen	graph:	https://github.com/jdevoo/twecoll
##	https://wakari.io/sharing/bundle/iuliacioroianu/Text_analysis_Python_NLTK

def	normalize_word(word):
		return	stemmer_func(word.lower())

def	get_words(titles):
	words	=	set()
	for	title	in	titles:
	
		for	word	in	title:
			words.add(normalize_word(word))
	return	list(words)
		
def	vectorspaced(title):
#			title_components	=	[normalize_word(word)	for	word	in	title[0].decode('utf-8').split()]
		title_components	=	[normalize_word(word)	for	word	in	title]
		return	np.array([
				word	in	title_components	and	not	word	in	stopwords
				for	word	in	words],	np.short)
				
				
def	write_tweets_df_todisk(tweets_df):
	tweets_df.to_csv('Results/tweets_collection.tsv',	sep='\t',	header=False,	index=False)

def	cluster_tweets_infile(in_tsv_fname=""):
	if	not	in_tsv_fname:
		print	'Not	a	valid	filename'
		return

	#	Read	the	input	TSV	file	with	user_names	and	tweet		
	df	=	pd.read_csv(	in_tsv_fname,	sep='\t',	header=None)
	df	=	df.dropna()
	df	=	df.drop_duplicates()
	df[2]	=	df[2].apply(lambda	tweet:	tweet.decode('utf-8'))

#		tweets	=	{}
#		for	x	in	rawLines:
#			match	=	re.search('^\s*[0-9]+\t',x)#re.search(r'\d+\t',	tweets)
#			if	match:
#				a	=	x.rstrip('\r\n').split('\t')
#				if	len(a)	==	2:	
#					tweets[a[0]]	=	a[1]
#					
#	
#		print	np.shape(rawLines),	'rawLines;',	np.shape(tweets),	'tweets'
#		
	global	stemmer_func,	words,	stopwords	
	
	stemmer_func	=	nltk.stem.snowball.SnowballStemmer("english").stem
	stopwords	=	set(nltk.corpus.stopwords.words('english'))
	
#		print	tweets[1]

	words	=	get_words(df[2].values)
	print	words[:10]

	#	K-Means	clustering:
	cluster	=	KMeansClusterer(7,	euclidean_distance,avoid_empty_clusters=True)
	#	GAAClusterer
	cluster	=	GAAClusterer(13)
	
	cluster.cluster([vectorspaced(title)	for	title	in	df[2].values	if	title],True)
	classified_examples	=	[cluster.classify(vectorspaced(title))	for	title	in	df[2].values]
	
	#	Display	clusters	/	write	to	disk
	with	open	('Results/clustered_relevant_users.tsv',	'w')	as	f:
		for	cluster_id,	title	in	sorted(zip(classified_examples,	df[2].values)):
			#print	cluster_id,	df[0].loc[df[1]	==	title].values,	title
			if	cluster_id	==	11:
				#	save:	docid	tab	userids	
				f.write('{}\t{}\n'.format(df[0].loc[df[2]	==	title].values,	df[1].loc[df[2]	==	title].values))
					
	print	type(classified_examples),	np.shape(classified_examples)
	import	os.path
	if	os.path.isfile('Results/clustered_relevant_users.tsv'):	print	'Wrote:	Results/clustered_relevant_users.tsv'
	
#		tweets_sanslinks=	df['1'].apply(lambda	tweet:	[tweet.strip(l)	for	l	in	re.findall(r'(https?://\S+)',	tweet)	if	not	l]	)
#	#		tweets_sanslinks=[x	for	x	in	tweets_sanslinks	if	not	x]
#		print	tweets_sanslinks[:20]
#		df['2']	=	df['1'].apply(lambda	tweet:	tweet.lstrip("[\'").rstrip("\']"))
#		print	[x.strip(l)	for	l	in	re.findall(r'(https?://\S+)',	row[''])]
#		tst_ar	=[]
#		for	row	in	df.iterrows():
#			print	row
#			if	re.findall(r'(https?://\S+)',	row['1']):
#				print	row['1']
#			else:
#				
#				
#			
#		
#		
	
	
	
	return	
	
def	get_parser():
	parser	=	argparse.ArgumentParser(description='procjson	clust	|	Ex:	python	procjson_clust.py	'+
																								'Results/tweets_cleaned.tsv')
	parser.add_argument('tsvfile',	metavar='TSVFILE',	help='Input	file:	tsv.')
	parser.add_argument('--version',	action='version',	version=__version__)
	return	parser
	
def	main():
	parser	=	get_parser()
	args	=	vars(parser.parse_args())
	
	cluster_tweets_infile(args['tsvfile'])
	
	if	not	args['tsvfile']:
			parser.print_help()
			os._exit(1)

if	__name__=='__main__':
	main()
	print	'Done'
