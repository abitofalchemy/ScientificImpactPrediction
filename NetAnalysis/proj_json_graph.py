import json, io
import pandas as pd
import numpy as np
import string, re

from pprint import pprint
from collections import defaultdict
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
plt.style.use('ggplot')

global clust, df
verbose = False

def jacc_coeff(words_set_a, words_set_b):
  if len(words_set_a) <1  or len(words_set_b) < 1:
    return
  a = frozenset((w for w in words_set_a))
  b = frozenset((w for w in words_set_b))
  jaccardcoefficent = (float(len(a & b)) / float(len (a|b)))
  return jaccardcoefficent

def average_jacc_dist(ref_doc, to_docs_arr):
	jac_vec = []
	for tid in to_docs_arr:
		#print df['twdoc'][df.index==int(tid)].values[0]
		jac_vec.append(jacc_coeff(ref_doc,df['twdoc'][df.index==int(tid)].values[0]))
	return np.mean(jac_vec)


def cluster(tid, doc):
	jacc_dist_vec = []
	for sid in seed_id_lst:
		centroid_arr = clust[sid]
		if len(centroid_arr) > 1:
			jacc_dist_vec.append(average_jacc_dist(doc,centroid_arr))
		else:
			#print df['twdoc'][df.index==int(sid)].values[0]
			seed_doc = df['twdoc'][df.index==int(sid)].values[0]
			jacc_dist_vec.append(jacc_coeff(doc,seed_doc))

	max_jacc_val = max(jacc_dist_vec)
	sid=  seed_id_lst[jacc_dist_vec.index(max_jacc_val)]
	
	return sid

# << Begin >>
#given_json_file = "Tweets.json"
given_text_file = "tweets.json"
#given_text_file = "datasets/isomorphism_quasipolynomial.json"

# reads in the JSON file
if 0:
  with open(given_text_file) as f:
    for line in f:
      a = json.dumps(json.JSONEncoder().encode(line.strip('\n')))
      print type(json.loads(a))
      b = json.loads(line)
      print type(b)
      break

data_json = io.open(given_text_file, mode='r', encoding='utf-8').read()
raw_tweets=data_json.splitlines()
#print raw_tweets[0]

docs =[]
tids =[]
links =[]
tw_dict = dict()

k = 0 
for d in raw_tweets:
# 	print d
#  a = json.dumps(d.replace("\'", '"'))
	print k
	k +=1 
	if not len(d):
		continue
	tw_d = json.loads(d.rstrip('\n'))
	tt = str(tw_d[u'text'].encode("utf-8"))
	lnks = re.findall(r'(https?://\S+)', tt) #re.search("(?P<url>https?://[^\s]+)", tt)
	if len(lnks):
		links.append(lnks)
	tt = tt.translate(None, string.punctuation)
	words_list = tt.split()
	# Filtered Words
	fw = [word for word in words_list if word not in stopwords.words('english')]
	docs.append( fw )
	# a dict with tweet id as the key and the filtered words as the values
	tw_dict[tw_d[u'id']] = fw
	tids.append( tw_d[u'id'] )
# ##


ix = tids.pop()
di = tw_dict.pop(ix)

Clusters = defaultdict(list)
Clusters[0] = {ix: di}

i = 0
while tids:
	jx = tids.pop()
	dj = tw_dict.pop(jx)
	jv_for_cluster = []
	jv = 0
	for c in Clusters.values():
		# Jaccard distance 1 - jaccard index
		jacc_vec = [jacc_coeff(dj, ixd[1]) for ixd in c.items()]
		jv = [1.0-x for x in jacc_vec]
		if len(jv)>1:
			print np.mean(jv)
			jv_for_cluster.append([np.mean(jv)])
		else:
			jv_for_cluster.append(jv)


	min_jv = np.min(jv_for_cluster)
	if (len(Clusters) <= 25) and (min_jv > 0.):
		Clusters[len(Clusters)] = {jx: dj}
	else: #if (len(Clusters) <= 25) and (jv > 0.):

		loci = jv_for_cluster.index(np.min(jv_for_cluster))
		elems = Clusters[loci]
		elems[jx] = dj
		Clusters[loci] = elems

with  open('kmeans_tw_clust.tsv', 'w') as f:
	for k,v in Clusters.items():
		[f.write('{0}\t{1}'.format(k+1, value)) for value in v.keys()]
		f.write('\n')
