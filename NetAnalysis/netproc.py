__author__ = 'saguinag'+'@'+'nd.edu'
__version__ = "0.1.0"

##
##  net_proc network process 
##

## TODO: some todo list
#

## VersionLog:
# 0.0.1 Initial commit
# Notes:
# http://scipy.github.io/old-wiki/pages/Cookbook/Matplotlib/Show_colormaps


import argparse,traceback,optparse
import time, os, sys,  csv, json
import pandas as pd 
import networkx as nx
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import re, datetime

# class EdgeListGraph():
#   '''
#   graphs_path Path where edgelist for ea. graph are found
#   '''
#   def __init__(self, edgelist_path):
#     self.edgelist_path = edgelist_path
#     self.G = nx.Graph()
    
#     with open(self.edgelist_path, 'rb') as f:
#       inreader = csv.reader(f, delimiter='\t')  
#       edges = []  
#       for row in inreader:
#         #print type(row[0])
#         if not row[0].startswith('%'):
#           edges.append((row[0],row[1]))
#     print edges
#     self.G.add_edges_from(edges)

    # return self.G

def twitter_authentication():
  fileNamePaht = ".env/keys.tsv"
  keys_dict = dict()
  with open(fileNamePaht, 'r') as f:
    inreader = csv.reader(f,delimiter='\t')
    for row in inreader:
      keys_dict[row[0]] = row[1]
    
    return keys_dict

def get_parser():
  parser = argparse.ArgumentParser(description='query twitter and output to file')
  parser.add_argument('--version', action='version', version=__version__)
  return parser

def main():
  edgelist_path = ["paper00_0.edgelist","Feb18_10_41paper00_0.edgelist","tweets_0.edgelist"]
  G = nx.Graph()
  f, axs = plt.subplots(1,1,figsize=(1.6*4,1.*4))
  
  for infile in edgelist_path:
    with open(infile, 'r') as f:
      inreader = csv.reader(f, delimiter='\t')  
      edges = []  
      for row in inreader:
        if not row[0].startswith('%'):
          edges.append((row[0],row[1]))
    #print edges
  
    G.add_edges_from(edges)
    print G.number_of_nodes()
    print G.number_of_edges()

    nx.draw_networkx(G,ax=axs,with_labels=False,font_size=8,node_size=20, alpha=0.75)
  
  # axs.grid(b= 'off')#, which ='both') 
  axs.get_xaxis().set_ticks([])
  axs.get_yaxis().set_ticks([])
  output_filename = 'outfile'
  plt.savefig( output_filename, bbox_inches='tight')

def paris():
  edgelist_path = ["paper00_0.edgelist","Feb18_10_41paper00_0.edgelist","tweets_0.edgelist",]
  edgelist_path = ["out.edgelist"]
  edgelist_path = ['../dataset/json-1458206289_13Apr16_131739.edglst']
  G = nx.Graph()
  f, axs = plt.subplots(1,1,figsize=(1.6*4,1.*4))
  
  for infile in edgelist_path:
    with open(infile, 'r') as f:
      inreader = csv.reader(f, delimiter='\t')  
      edges = []
      user_v= {} 
      for row in inreader:
        if not row[0].startswith('%'):
#          print row
          edges.append((row[0],row[1]))
          user_v[row[0]] = 1
#    print G.nodes()
    G.add_edges_from(edges)
    print G.number_of_nodes()
    print G.number_of_edges()
    values = [user_v.get(v,0.125) for v in G.nodes()]

    
#    nx.draw_networkx(G,ax=axs,with_labels=False,font_size=8,node_size=20, alpha=0.75)
    nx.draw_networkx(G,ax=axs,cmap=plt.get_cmap('flag'), node_color=values,pos=nx.spring_layout(G), with_labels=False,font_size=8,node_size=10,alpha=0.7)

  # axs.grid(b= 'off')#, which ='both') 
  axs.get_xaxis().set_ticks([])
  axs.get_yaxis().set_ticks([])
  axs.set_title('Sparse graph: Users discussing an article')
  axs.set_xlabel('Users (red) and Citing article (blue)')
  output_filename = 'outfig'
  plt.savefig( output_filename, bbox_inches='tight')
  print output_filename

if __name__ == '__main__':

  #main()
  paris()
  print 'Done.'
  sys.exit(0)

