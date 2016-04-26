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
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import pylab
pylab.rcParams['xtick.major.pad']='8'
pylab.rcParams['ytick.major.pad']='8'

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

def draw_citedby_graph(df=None):
	if df is None:
		return

	import networkx as nx

	# edges = np.array([df[0].values,df.])
	G = nx.Graph()
	conv_toInt = lambda x: int(x)
	df['uid'] = df['usr'].apply(conv_toInt)
	print df.dtypes
	edges = df[[0,'uid']].values

	G.add_edges_from(edges)

	f, axs = plt.subplots(1,1,figsize=(1.6*4,1*4))
	p = nx.spring_layout(G)
	nx.draw_networkx_edges(G,pos=p, ax=axs,edge_color='darkgray', width=0.7, alpha=.7)
	nx.draw_networkx_nodes(G,pos=p, ax=axs,
    node_size=20,
  	node_color=G.nodes(),cmap=plt.cm.Reds_r)
	# nx.draw_networkx(G, ax=axs,node_size=30, with_labels=False)
	# nx.draw_networkx_edges(G, ax=axs, width=0.5)
	axs.patch.set_facecolor('None')
	axs.set_xticks([])
	axs.set_yticks([])

	plt.grid(0)
	plt.savefig('outfig.pdf', bbox_inches='tight')

	# get the LCC
	lgcsg_d = {}
	lgc_graphs= list(nx.connected_component_subgraphs(G))
	for i,g in enumerate(lgc_graphs):
		#print i, g.number_of_nodes()
		if i == 0:
			lgc_graphs[0] = (g.number_of_nodes(),g)
			continue
		if g.number_of_nodes() > lgc_graphs[0][1].number_of_nodes():
			lgc_graphs[1] = lgc_graphs[0]
			lgc_graphs[0] = (g.number_of_nodes(),g)

	# print lgc_graphs[0][1].number_of_nodes()
	# print lgc_graphs[1][1].number_of_nodes()

	import net_metrics as metrics

	metrics.draw_degree_probability_distribution(lgc_graphs[0][1])
	metrics.draw_clustering_coefficients(lgc_graphs[0][1])
	metrics.draw_kcore_decomposition(lgc_graphs[0][1])
	metrics.draw_assortativity_coefficients(lgc_graphs[0][1])





def proc_clusters(in_fname = None):
	if in_fname is None:
		return

	df = pd.DataFrame.from_csv(in_fname, sep='\t',index_col=False,header=None)
	# df['twt_id'] = [x[1] for x in df[1]]
	# df['usr_id'] = df[1][0]
	print [x.lstrip('(').rstrip(')') for x in df[1][0].split(', ')]

	un_tuple = lambda x: x.split(', ')
	rem_parens = lambda x: x.lstrip('(').rstrip(')')
	df['usr_twt'] = df[1].apply(rem_parens).apply(un_tuple)
	# df['usr_id'] = df['usr_twt']
	#print df.head()

	# print df['usr_twt'].head()
	print
	citedby_usrid = lambda x: x[0]
	df['usr'] = df['usr_twt'].apply(citedby_usrid)
	# clus_citedby_usrid = lambda x:  (x[0],x[1])
	# print df[[0,'usr']].head()
	# print df[[0,'usr']].apply(clus_citedby_usrid)
	df[[0,'usr']].to_csv(in_fname.rstrip('.tsv')+'_out.tsv',
											 sep='\t',
											 header=None,
											 index=False)

	draw_citedby_graph(df)

if __name__ == '__main__':

	#main()
	proc_clusters('../dataset/clusters_18Apr.tsv')
	print 'Done.'
	sys.exit(0)

	# import networkx as nx
	# nx.random_degree_sequence_graph('../dataset/clusters_18Apr.tsv')