#	-*-	coding:	utf-8	-*-

__author__	=	'Sal	Aguinaga'
__license__	=	"GPL"
__version__	=	"0.1.0"
__email__		=	"saguinag@nd.edu"

import	pprint	as	pp
import	pandas	as	pd
import	numpy	as	np
import  scipy
from	nltk.cluster	import	KMeansClusterer,	GAAClusterer,	euclidean_distance
import	nltk.corpus
import	nltk.stem
import distance

import	re
import	io
import	json,	time,	sys,	csv
from	HTMLParser	import	HTMLParser

import	sys,	os,	argparse
import	traceback
import	time,	datetime
import	ast
import	glob
from collections import defaultdict
import	matplotlib
matplotlib.use('pdf')
import	matplotlib.pyplot	as	plt
plt.style.use('ggplot')

global cDict;

##	http://stackoverflow.com/questions/23531608/how-do-i-save-streaming-tweets-in-json-via-tweepy
##	https://www.airpair.com/python/posts/top-mistakes-python-big-data-analytics
##	Gen	graph:	https://github.com/jdevoo/twecoll
##	https://wakari.io/sharing/bundle/iuliacioroianu/Text_analysis_Python_NLTK
# def jacc_dist_cluster(nK, dfrow, cDict):
#   print len(cDict)
#   if len(cDict) < 1:
#     cDict[1] = (dfrow[0], dfrow[1])
#   else:
#     print 'clustering: ', dfrow[2]
#     for k,v in cDict.items():
#       jDist = distance.jaccard(dfrow[2], cDict[k]])


def cluster_doc_collection(nbrK, clust_method, pndsDF):
  if clust_method != 'jacc':
    return

  df = pndsDF
  df = df.sort_values(by=[2])



  cDict = defaultdict(list)
  #df.apply(lambda row: jacc_dist_cluster(nbrK, row, cDict=cDict), axis=1)
  for dfrow in df.iterrows():
    # print dfrow[0], dfrow[1][1]

    # if dfrow[0] > 15: break
    # -- the first case
    if len(cDict) < 1:
      cDict[1].append(dfrow[1][1])
      continue

    tid_added_bool = False
    for k in cDict.keys():
      # print "key",k, len(cDict[k])
      jDVals = []

      if len(cDict[k]) > 1:
        # print [df.loc[df[1] == y[1]][2].values[0].encode('utf-8') for y in cDict[k]]
        jDVals.append([distance.jaccard(dfrow[1][2], df.loc[df[1] == y][2].values[0].encode('utf-8')) for y in cDict[k]])
        jDist = np.mean(jDVals)
      else:
        jDist = distance.jaccard(dfrow[1][2], str(df.loc[df[1] == cDict[k][0]][2].values[0].encode('utf-8')))

      if ((k-1)/float(nbrK) > jDist) and (jDist < k/float(nbrK)):
        cDict[k].append(dfrow[1][1])
        tid_added_bool = True

    if (len(cDict) < nbrK) and not tid_added_bool:
      cDict[len(cDict.keys())+1].append(dfrow[1][1])
    # print dfrow[0], cDict.keys()
    # print("  {}".format(cDict))

  for k,v in cDict.items():
    for x in v:
      print k, df.loc[df[1] == x][2].values[0].encode('utf-8')
  # print len(cDict.values())
  exit()
  idx = np.arange(len(pndsDF))
  np.random.shuffle(idx)
  seed_clusters = df.loc[df.index.isin(idx[:nbrK])]
  seed_clusters['cltrs'] = range(len(seed_clusters))

  # clustersDict={}
  #
  # for j,clst in enumerate(seed_clusters.index.values):
  #   # Here I need to compare strings using levenstein or Jaccard similarity
  #   jacc_dist = df.apply(lambda doc: distance.jaccard(doc[2], df.iloc[clst][2]), axis=1)
  #
  #   # clustersDict[clust]=[x for x in jacc_dist.values if ((j/float(nbrK) > x) and ((j+1.)/float(nbrK) <x))]
  #   # print [x for x in jacc_dist.values if x < 1/float(nbrK)]
  #
  #   break

  exit()
  return

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

def extract_tweets_citedby_graph(df):
  global	stemmer_func,	words,	stopwords

  stemmer_func	=	nltk.stem.snowball.SnowballStemmer("english").stem
  stopwords	=	set(nltk.corpus.stopwords.words('english'))

  words	=	get_words(df[2].values)
  # pp.pprint(words[:10])

  #	K-Means	clustering:
  # cluster	=	KMeansClusterer(7,	euclidean_distance,avoid_empty_clusters=True)

  #	GAAClusterer
  cluster	=	GAAClusterer(21)

  cluster.cluster([vectorspaced(title)	for	title	in	df[2].values	if	title],True)
  classified_examples	=	[cluster.classify(vectorspaced(title))	for	title	in	df[2].values]

  # for	cluster_id,	title	in	sorted(zip(classified_examples,	df[2].values)):
  #   # print	"{}\t{}\t{}\n".format(cluster_id,	df[0].loc[df[2]	==	title].values,	df[1].loc[df[2]	==	title].values)
  #   print	"{}\t{}\t{}".format(cluster_id,	df[1].loc[df[2]	==	title].values, title)

  #	Display	clusters	/	write	to	disk
  with	open	('Results/clustered_relevant_users.tsv', 'w')	as f:
    for	cluster_id,title in sorted(zip(classified_examples,	df[2].values)):
      if	cluster_id>6:
        #	save:	docid	tab	userids
        f.write('{}\t{}\n'.format(df[0].loc[df[2]	==	title].values,	df[1].loc[df[2]	==	title].values))
  if os.path.exists('Results/clustered_relevant_users.tsv'):  print 'file saved: Results/clustered_relevant_users.tsv'

  return


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

  seed_filter = "Graph Isomorphism in Quasipolynomial Time Laszlo Babai"

  df['jacc_dist'] = df.apply(lambda row: distance.jaccard(seed_filter, row[2]), axis=1)#
  print df['jacc_dist'].describe()
  print df.loc[df['jacc_dist']< 0.52][2]
  if 1:
    extract_tweets_citedby_graph(df.loc[df['jacc_dist']< 0.52])
  else:
    df[2]	=	df[2].apply(lambda	tweet:	tweet.decode('utf-8'))
    cluster_doc_collection(21,'jacc',pndsDF=df)

  exit()


#   global	stemmer_func,	words,	stopwords
#
#   stemmer_func	=	nltk.stem.snowball.SnowballStemmer("english").stem
#   stopwords	=	set(nltk.corpus.stopwords.words('english'))
#
# #		print	tweets[1]
#
#   words	=	get_words(df[2].values)
#   print	words[:10]
#
#   #	K-Means	clustering:
#   cluster	=	KMeansClusterer(7,	euclidean_distance,avoid_empty_clusters=True)
#   #	GAAClusterer
#   cluster	=	GAAClusterer(13)
#
#   cluster.cluster([vectorspaced(title)	for	title	in	df[2].values	if	title],True)
#   classified_examples	=	[cluster.classify(vectorspaced(title))	for	title	in	df[2].values]
#
#   #	Display	clusters	/	write	to	disk
#   with	open	('Results/clustered_relevant_users.tsv',	'w')	as	f:
#     for	cluster_id,	title	in	sorted(zip(classified_examples,	df[2].values)):
#       #print	cluster_id,	df[0].loc[df[1]	==	title].values,	title
#       if	cluster_id	==	11:
#         #	save:	docid	tab	userids
#         f.write('{}\t{}\n'.format(df[0].loc[df[2]	==	title].values,	df[1].loc[df[2]	==	title].values))
#
#   print	type(classified_examples),	np.shape(classified_examples)
#   import	os.path
#   if	os.path.isfile('Results/clustered_relevant_users.tsv'):	print	'Wrote:	Results/clustered_relevant_users.tsv'

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
