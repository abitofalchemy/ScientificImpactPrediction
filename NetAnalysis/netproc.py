__author__ = 'saguinag' + '@' + 'nd.edu'
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


import argparse, traceback, optparse
import time, os, sys, csv, json
import pandas as pd
import networkx as nx
import matplotlib
import pprint as pp
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
    inreader = csv.reader(f, delimiter='\t')
    for row in inreader:
      keys_dict[row[0]] = row[1]

    return keys_dict


def get_parser():
  parser = argparse.ArgumentParser(description='query twitter and output to file')
  parser.add_argument('--version', action='version', version=__version__)
  return parser


def main():
  edgelist_path = ["paper00_0.edgelist", "Feb18_10_41paper00_0.edgelist", "tweets_0.edgelist"]
  G = nx.Graph()
  f, axs = plt.subplots(1, 1, figsize=(1.6 * 4, 1. * 4))

  for infile in edgelist_path:
    with open(infile, 'r') as f:
      inreader = csv.reader(f, delimiter='\t')
      edges = []
      for row in inreader:
        if not row[0].startswith('%'):
          edges.append((row[0], row[1]))
    # print edges

    G.add_edges_from(edges)
    print G.number_of_nodes()
    print G.number_of_edges()

    nx.draw_networkx(G, ax=axs, with_labels=False, font_size=8, node_size=20, alpha=0.75)

  # axs.grid(b= 'off')#, which ='both') 
  axs.get_xaxis().set_ticks([])
  axs.get_yaxis().set_ticks([])
  output_filename = 'outfile'
  plt.savefig(output_filename, bbox_inches='tight')


def paris():
  edgelist_path = ["paper00_0.edgelist", "Feb18_10_41paper00_0.edgelist", "tweets_0.edgelist", ]
  edgelist_path = ["out.edgelist"]
  edgelist_path = ['../dataset/json-1458206289_13Apr16_131739.edglst']
  G = nx.Graph()
  f, axs = plt.subplots(1, 1, figsize=(1.6 * 4, 1. * 4))

  for infile in edgelist_path:
    with open(infile, 'r') as f:
      inreader = csv.reader(f, delimiter='\t')
      edges = []
      user_v = {}
      for row in inreader:
        if not row[0].startswith('%'):
          #          print row
          edges.append((row[0], row[1]))
          user_v[row[0]] = 1
        #    print G.nodes()
    G.add_edges_from(edges)
    print G.number_of_nodes()
    print G.number_of_edges()
    values = [user_v.get(v, 0.125) for v in G.nodes()]

    #    nx.draw_networkx(G,ax=axs,with_labels=False,font_size=8,node_size=20, alpha=0.75)
    nx.draw_networkx(G, ax=axs, cmap=plt.get_cmap('flag'), node_color=values, pos=spring_layout(G),
                  with_labels=False, font_size=8, node_size=10, alpha=0.7)

  # axs.grid(b= 'off')#, which ='both') 
  axs.get_xaxis().set_ticks([])
  axs.get_yaxis().set_ticks([])
  axs.set_title('Sparse graph: Users discussing an article')
  axs.set_xlabel('Users (red) and Citing article (blue)')
  output_filename = 'outfig'
  plt.savefig(output_filename, bbox_inches='tight')
  print output_filename

def clustered():

  f, axs = plt.subplots(1, 1, figsize=(1.6 * 4, 1. * 4))


  # with open('../data_collection/' + infile) as f:
  #   inreader = csv.reader(f, delimiter="\t")
  #   edges = []
  user_v = {}
  #
  #   for row in inreader:
  #     if not row[0].startswith('%'):
  #       print (int(row[0]), int(row[1]))
  #       edges.append((int(row[0]), int(row[1])))
  #       user_v[int(row[0])] = 1
  #     #    print G.nodes()
  # G.add_edges_from(edges)
  # print type(infile), infile

  G = nx.read_edgelist("../data_collection/iso_morph_laszlo_babai_apoll_clusters.edgelist", delimiter=',')
  print G.number_of_nodes()
  print G.number_of_edges()
  exit()

  n = G.number_of_nodes()
  ## Position nodes using a random geometric graph
  # GG= random_geometric_graph(n, 0.5)
  # gpos= get_node_attributes(GG, 'pos')
  # # find node near center (0.5,0.5)
  # dmin=1
  # ncenter=0
  # for n in gpos:
  #     x,y=gpos[n]
  #     d=(x-0.5)**2+(y-0.5)**2
  #     if d<dmin:
  #         ncenter=n
  #         dmin=d
  # # # color by path length from node near center
  # p=nx.single_source_shortest_path_length(GG,ncenter)

  for e in G.edges():
    user_v[e[0]] = 1
  values = [user_v.get(v, 0.125) for v in G.nodes()]

  #    nx.draw_networkx(G,ax=axs,with_labels=False,font_size=8,node_size=20, alpha=0.75)
  gpos = nx.random_layout(G)
  nx.draw_networkx(G, pos=gpos, ax=axs, cmap=plt.get_cmap('flag'), node_color=values,
                with_labels=False, font_size=8, node_size=20, alpha=0.7)
  # nx.draw_networkx_edges(G, gpos, ax=axs, edge_color='lightgray', width=1., alpha=0.5)
  # nx.draw_networkx_nodes(G, gpos, nodelist=p.keys(),
   #                        node_size=80,
   #                        node_color=G.nodes(),
   #                        cmap=plt.get_cmap('flag'))

  # axs.grid(b= 'off')#, which ='both')
  axs.get_xaxis().set_ticks([])
  axs.get_yaxis().set_ticks([])
  axs.patch.set_facecolor('None')
  # axs.set_title('Sparse graph: Users discussing an article')
  # axs.set_xlabel('Users (red) and Citing article (blue)')

  pp.pprint(G.edges())
  output_filename = 'outfig'
  plt.savefig(output_filename, bbox_inches='tight')
  print output_filename

def halyard():
  edgelist_path = ["paper00_0.edgelist", "Feb18_10_41paper00_0.edgelist", "tweets_0.edgelist", ]
  edgelist_path = ["out.edgelist"]
  edgelist_path = ['../data_collection/json-1458206289_13Apr16_131739.edglst']
  edgelist_path = ['../data_collection/iso_morph_laszlo_babai_apolluniq_claims.edgelist',\
                   '../data_collection/iso_morph_laszlo_babai_apoll_clusters.edgelist']

  # G = nx.Graph()
  f, axs = plt.subplots(1, 1, figsize=(1.6 * 4, 1. * 4))

  for i, infile in enumerate(edgelist_path):
    print  infile,'~'*20
    # with open('../data_collection/' + infile) as f:
    #   inreader = csv.reader(f, delimiter="\t")
    #   edges = []
    user_v = {}
    #
    #   for row in inreader:
    #     if not row[0].startswith('%'):
    #       print (int(row[0]), int(row[1]))
    #       edges.append((int(row[0]), int(row[1])))
    #       user_v[int(row[0])] = 1
    #     #    print G.nodes()
    # G.add_edges_from(edges)
    print type(infile), infile

    G = nx.read_edgelist(infile, delimiter=',',nodetype=int)
    print G.number_of_nodes()
    print G.number_of_edges()
    n = G.number_of_nodes()
    ## Position nodes using a random geometric graph
    # GG= random_geometric_graph(n, 0.5)
    # gpos= get_node_attributes(GG, 'pos')
    # # find node near center (0.5,0.5)
    # dmin=1
    # ncenter=0
    # for n in gpos:
    #     x,y=gpos[n]
    #     d=(x-0.5)**2+(y-0.5)**2
    #     if d<dmin:
    #         ncenter=n
    #         dmin=d
    # # # color by path length from node near center
    # p=nx.single_source_shortest_path_length(GG,ncenter)

    for e in G.edges():
      user_v[e[0]] = 1
    values = [user_v.get(v, 0.125) for v in G.nodes()]

    #    nx.draw_networkx(G,ax=axs,with_labels=False,font_size=8,node_size=20, alpha=0.75)
    gpos = nx.random_layout(G)
    nx.draw_networkx(G, pos=gpos, ax=axs, cmap=plt.get_cmap('flag'), node_color=values,
                  with_labels=False, font_size=8, node_size=20, alpha=0.7)
    # nx.draw_networkx_edges(G, gpos, ax=axs, edge_color='lightgray', width=1., alpha=0.5)
    # nx.draw_networkx_nodes(G, gpos, nodelist=p.keys(),
		 #                        node_size=80,
		 #                        node_color=G.nodes(),
		 #                        cmap=plt.get_cmap('flag'))

    # axs.grid(b= 'off')#, which ='both')
    axs.get_xaxis().set_ticks([])
    axs.get_yaxis().set_ticks([])
    axs.patch.set_facecolor('None')
    # axs.set_title('Sparse graph: Users discussing an article')
    # axs.set_xlabel('Users (red) and Citing article (blue)')

    pp.pprint(G.edges())
  output_filename = 'outfig'
  plt.savefig(output_filename, bbox_inches='tight')
  print output_filename


if __name__ == '__main__':
  # main()
  # paris()
  #halyard()
  clustered()
  print 'Done.'
  sys.exit(0)
