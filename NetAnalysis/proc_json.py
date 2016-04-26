import json
import os
import io
import pandas as pd
import numpy as np
import string, re
import ast
from pprint import pprint
from collections import defaultdict
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import sandbox as sb
# from twtokenize import Tokenizer

import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
plt.style.use('ggplot')

global clust, df
verbose = False
"""
  http://stackoverflow.com/questions/1789254/clustering-text-in-python
  
  alt
  https://www.daniweb.com/programming/software-development/code/216641/statistical-learning-with-python-clustering
  http://marcobonzanini.com/2015/03/17/mining-twitter-data-with-python-part-3-term-frequencies/
  http://www.bogotobogo.com/python/scikit-learn/scikit_machine_learning_Unsupervised_Learning_Clustering.php
  
"""


def drop_duplicates(doclist):
  df = pd.DataFrame(doclist)
  df = df.drop_duplicates()
  return df


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

emoticons_str = r"""
  (?:
  [:=;] # Eyes
  [oO\-]? # Nose (optional)
  [D\)\]\(\]/\\OpP] # Mouth
  )"""

regex_str = [
             emoticons_str,
             r'<[^>]+>', # HTML tags
             r'(?:@[\w_]+)', # @-mentions
             r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
             r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
             
             r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
             r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
             r'(?:[\w_]+)', # other words
             r'(?:\S)' # anything else
             ]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
  return tokens_re.findall(s)

def preprocess(s, lowercase=False):
#  s = str(s.encode("utf-8"))
#  s = str(s).translate(None, string.punctuation)
#   print s[-1]
  tokens = tokenize(s)
  # print tokens[-1]
  # exit()
  if lowercase:
    tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
  return tokens

def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

# << Main >>
# << Begin >>

#given_text_file = "../data_collection/json-1458206289.json"
#given_text_file = "../data_collection/paper_accepted.json"
given_text_file = "../../data_collection/tweets.json"
given_text_file = "../datasets/isomorphism_quasipolynomial.json"
given_text_file = "../datasets/iso_morph_laszlo_babai_apollo.json"
ds_name = os.path.basename(given_text_file).rstrip('.json')




# reads in the JSON file
if 0:
  altm_tq = []
  with open ('../dataset/altmetric_tq.txt') as f:
    for l in f:
      altm_tq.append(l.rstrip('\r\n'))
  # print len(altm_tq)

  print type ( json.load(given_text_file))
  # with open(given_text_file) as f:
  #   data = []
  #   for line in f:
  #       a = json.dumps(line.rstrip('\n'))
  #       b = json.loads(a)
  #       print type(a)

  #       break
  # print  a
  #   for line in f:
  #     a = json.loads(json.JSONEncoder().encode(line.strip('\r\n')))
  #     # rtweets = ast.literal_eval(line.strip('\r\n'))
  #     # tw = json.loads(line.strip('\r\n'))
  #     tw = json.loads(a)
  #     # print rtweets
  #     break
  # print tw

  # for tq in altm_tq:
  #   # print jacc_coeff(tq,tq)
  #   if jacc_coeff(set(tw['text']),set(tq)) > .6:
  #     print json.JSONEncoder().encode(tw['text']),'\n\t', tq
  # with open(given_text_file) as f:
  #   for line in f:
  #     tw = json.loads(line.strip('\r\n'))
  #     for tq in altm_tq:
  #       # print jacc_coeff(tq,tq)
  #       if jacc_coeff(set(tw['text']),set(tq)) > .6:
  #         print json.JSONEncoder().encode(tw['text']),'\n\t', tq
hlinks = []
docsd  = {}
twbyuser_tw_id = []

if 0:

  # tok = Tokenizer(preserve_case=False)
  with open(given_text_file) as f:
    i = 0
    for line in f:
      a = json.loads(json.JSONEncoder().encode(line.strip('\r\n')))
      rtweets = ast.literal_eval(line.strip('\r\n'))
      lnks = re.findall(r'(https?://\S+)', rtweets['text'])
      hlinks.append(lnks)
      tokens = preprocess(rtweets['text'])
      tokens = [word for word in tokens if word not in stopwords.words('english')]
      tokens = [str(json.JSONEncoder().encode(s)).translate(None, string.punctuation) for s in tokens]
      if lnks:
        [tokens.remove(l) for l in lnks if l in tokens]
        
      #print(rtweets['user']['id'],rtweets['id']) # value user_id cites tweet_id
      docsd[' '.join(tokens)] = (rtweets['user']['id'],rtweets['id'])
      twbyuser_tw_id.append([ ' '.join(tokens), rtweets['user']['id'],rtweets['id']])
      i += 1
      if i > 10: break
else:
  # read apollo
  data_json = io.open(given_text_file, mode='r', encoding='utf-8').read()
  raw_tweets=data_json.splitlines()
  print 'read json lines into a list.'
  i = 0
  for tw in raw_tweets:
    rtweets = json.loads(tw)
    lnks = re.findall(r'(https?://\S+)', rtweets['text'])
    hlinks.append(lnks)
    tokens = preprocess(rtweets['text'])
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    tokens = [str(json.JSONEncoder().encode(s)).translate(None, string.punctuation) for s in tokens]
    if lnks:
      [tokens.remove(l) for l in lnks if l in tokens]

    #print(rtweets['user']['id'],rtweets['id']) # value user_id cites tweet_id
    docsd[' '.join(tokens)] = (rtweets['user']['id'],rtweets['id'])
    twbyuser_tw_id.append([ ' '.join(tokens), rtweets['user']['id'],rtweets['id']])
    i += 1


print len(docsd), len(hlinks), len(twbyuser_tw_id)
## 17 5954 5954

df = pd.DataFrame(twbyuser_tw_id)
print df.shape
df = df.drop_duplicates()
print df.shape
# df = pd.DataFrame.from_dict(docsd.items())
# print '',df.shape
# df = df.drop_duplicates()
# print '',df.shape


#df = pd.DataFrame.from_dict(docsd.items())
df[[1,2]].to_csv("../data_collection/"+ds_name+"uniq_claims.edgelist",header=False,index=False)

if 1:
  # http://brandonrose.org/clustering

  #documents = [{"text": text, "tokens": text.split('\t')} for i, text in enumerate(docs)]
  # documents = [{"text": ' '.join(text), "tokens": text} for i, text in enumerate(docs)]
  documents = [{"text": text, "tokens": text.split()} for i, text in enumerate(docsd.keys())]


  sb.add_tfidf_to(documents)
  dist_graph = sb.get_distance_graph(documents)

  j = 0
  with open ("../data_collection/"+ds_name+'_clusters.edgelist', 'w') as f:
    for cluster in sb.majorclust(dist_graph):
      print j,"========="
      for doc_id in cluster:
          # userid = [k for k,v in user_claims_d.iteritems() if v == documents[doc_id]["tokens"]]
    #      print doc_id,'cites', userid,documents[doc_id]["text"]
          userid = docsd[documents[doc_id]["text"]][0]
          print userid, 'cites_cluster', j, documents[doc_id]["text"]
          f.write('{0}\t{1}\n'.format(userid,j))
      j +=1

#with open ('../datasets/altmetric_tq.txt') as f:
#  for l in f:
#    print l

# exit()
#
# data_json = io.open(given_text_file, mode='r', encoding='utf-8').read()
# raw_tweets=data_json.splitlines()
# print 'read json lines into a list.'
#
# docs =[]
# tids =[]
# links =[]
# tweet_d = dict()
# user_claims_d = {}
#
# k=0
# for d in raw_tweets:
#   if not len(d):    continue
#   #print k,
#   k+=1
#   tweet = json.loads(d.rstrip('\r\n'))
#   #docs.append(tweet['text'])
#   tokens = preprocess(tweet['text'])
#
#
#   lnks = re.findall(r'(https?://\S+)', tweet['text'])
# #  print lnks
#   #lnks = [re.findall(r'(https?://\S+)', tok) for tok in tokens] # re.search("(?P<url>https?://[^\s]+)", tt)
#   lnks = [l for l in lnks if len(l) is not 0]
#   if len(lnks):                            # dropping links from tweet string
#     links.append(lnks)
#     [tokens.remove(l) for l in lnks if l in tokens]
#
#   if not len(tokens): continue
#
#   tokens = [word for word in tokens if word not in stopwords.words('english')]
#   tweet_d[tweet['id']] = tokens
#   user_claims_d[tweet['user']['id']] = tokens
#   docs.append(tokens)
#
# print len(docs)
# doc_vecs = drop_duplicates(docs).values
# print len(docs)
# for d in docs:
#   print d
# exit()
# result = {}
# for key,value in tweet_d.items():
#   if value not in result.values():
#     result[key] = value

#print len(result)
#pprint (result)
