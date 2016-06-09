import shelve
import numpy as np 
import pandas as pd
import networkx as nx
import math 
import sa_net_metrics as snm
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# Links: http://www.programcreek.com/python/example/5240/numpy.loadtxt

def convert_follower_network_2edgelist():
  dbg = False
  df = pd.read_csv('Results/twtrs_follower_network.tsv', sep='\t',header=None )

  edges = []
  with open('Results/procjson.tsv','w') as fout:
    for row in df.iterrows():
      # get a count of the followers : a naive approach 
      users_flist = np.array([long(x) for x in row[1][1].lstrip('[').rstrip(']').split(',')])
      sampsize = int(math.ceil(len( users_flist) * .10))
      # pick 10% of their follower network at random
      if len(users_flist) > 1:
        idx = np.arange(len(users_flist))
        np.random.shuffle(idx)
        subsample = users_flist[idx[:sampsize]]
      else:
        subsample = users_flist

      # now get the network for submample
      for j, trg in enumerate(subsample):
        fout.write('{}\t{}\n'.format(row[1][0], trg)) #ong(trg.strip())))
        
        edges.append((row[1][0], trg))
      if dbg:  print row[1][0], len(row[1][1].lstrip('[').rstrip(']').split(','))
    if dbg: print len(edges)
  return edges

def visualize_graph(graph):
  if graph is None: return
  G  = graph
  # identify largest connected component

  Gcc=sorted(nx.connected_component_subgraphs(G), key = len, reverse=True)
  print [len(x) for x in Gcc]
  Gcc = Gcc[0]
  print nx.info(Gcc)
  print 'A' 
  pos=nx.circular_layout(Gcc)
  print 'B'
  nx.draw_networkx(Gcc, pos, with_labels=False, width=0.125, node_size=20, alpha=0.5)
  #nx.draw(Gcc, pos=nx.spring_layout(G))
  # print saving to disk
  print 'Saving to disk ...'
  plt.savefig('outplot',bb__inches='tight')




  df = pd.DataFrame.from_dict(G.degree().items())
  df.columns =['v','k']
  gb = df.groupby(['k']).count()
  gb['pk'] = gb/float(G.number_of_nodes())
  print gb.head(), '<= gb'
  #gb['deg'] = gb.index.values
  print gb.head()

  gb['pk'].to_csv('Results/degree.tsv', index=True, sep="\t", header=True)


  # draw graph
  #G=nx.random_geometric_graph(G.number_of_nodes(),0.125)
  # position is stored as node attribute data for random_geometric_graph
  #pos=nx.get_node_attributes(G,'pos')
  nx.draw_networkx(G, pos=nx.spring_layout(G), node_size=20, with_labels=False,  alpha=0.75, weight=0.5)
  # print saving to disk
  print 'Saving to disk ...'
  plt.savefig('outplot',bb__inches='tight')

if __name__ == '__main__':
  #convert_follower_network_2edgelist()
  
  infname = 'Results/procjson.tsv'
  if 1:
    G = nx.read_edgelist(infname)
    print nx.info(G)
    # Graph adj matix
    A = nx.to_scipy_sparse_matrix(G)
    print type(A)
    from scipy import sparse, io
    io.mmwrite("Results/test.mtx", A)
    exit()
    # write to disk clustering coeffs for this graph
    snm.get_clust_coeff([G], 'orig', 'mmonth')
    # write to disk egienvalue
    snm.network_value_distribution([G], [], 'origMmonth')
        
  if 0:
    edgelist= np.loadtxt(infname,dtype=str, delimiter='\t')
    print edgelist[:4]
    idx = np.arange(len(edgelist))
    np.random.shuffle(idx)
    subsamp_edgelist = edgelist[idx[:100]]
    G = nx.Graph()
    G.add_edges_from([(long(x),long(y)) for x,y in subsamp_edgelist])
  
  # visualize this graph 
  # visualize_graph(G)
  exit()
  
  G = nx.Graph()
  G.add_edges_from([(long(x),long(y)) for x,y in edgelist])
  print nx.info(G)
  print 'Done'  

