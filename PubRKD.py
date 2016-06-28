'''
# PubRKD

- author: "S.Aguinaga"
- date: "June, 2016"
- description: "Published Research Knowledge Discovery & Potential Impact"

'''

from procjson_clean import procjson_cleaned_docs_from
datasets_path = "datasets/"               # json datasets
procjson_cleaned_docs_from(datasets_path) # read raw (json) and ouput cleaned docs 

from procjson_clust import cluster_tweets_infile
cln_docs_tsv = "Results/tweets_cleaned.tsv"
cluster_tweets_infile(cln_docs_tsv)       # generates Results/clustered_relevant_users.tsv 
# for these users we can find their network

from procjson_fllwrnet import given_screenname_getfollowers
# get user_id's follower network (their twitter user ids)
given_screenname_getfollowers()           # generates tsv: twtrs_follower_network.tsv 


