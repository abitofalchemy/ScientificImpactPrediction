import shelve
import numpy as np
import pandas as pd
import networkx as nx
import math
import sa_net_metrics as snm
import matplotlib
import itertools
import pprint as pp
matplotlib.use('pdf')
import matplotlib.pyplot as plt

plt.style.use('ggplot')


# Links:
# [0] http://www.programcreek.com/python/example/5240/numpy.loadtxt
# [1] http://stackoverflow.com/questions/35782251/python-how-to-color-the-nodes-of-a-network-according-to-their-degree/35786355

def draw_citing_users_follower_count():
  df = pd.read_csv('Results/twtrs_follower_network.tsv', sep='\t', header=None)
  df.columns = ['src', 'followers']

  count_followers = lambda row: len(row[1].split(','))
  df['fCnt'] = df.apply(count_followers, axis=1)

  edglstdf = pd.read_csv('Results/clustered_relevant_users.tsv', sep='\t', header=None)
  eldf = edglstdf.apply(lambda row: [x.lstrip('[').rstrip(']') for x in row])
  eldf.columns = ['src','trg']


  eldf[['src']] = eldf[['src']].apply(pd.to_numeric)
  df = pd.merge(eldf,df, on='src')
  df[['src','trg','fCnt']].to_csv('Results/procjson_edglst.tsv', sep='\t', header=False, index=False)

  g=nx.Graph()
  g.add_edges_from(df[['src','trg']].values)
  print nx.info(g)

  f, axs = plt.subplots(1, 1, figsize=(1.6*6., 1*6.))
  # nx.draw_networkx(g, pos=nx.spring_layout(g), ax=axs,  with_labels=False, node_size=df[['fCnt']]/float(len(df)), alpha=.5)
  pos=nx.spring_layout(g)
  # nx.draw_networkx(g, pos=pos, ax=axs, with_labels=False, alpha=.5, node_size=30)
  nx.draw_networkx_edges(g, pos=pos, ax=axs, alpha=0.5, width=0.8)
  nx.draw_networkx_nodes(g, pos=pos, ax=axs, nodelist=list(df['src'].values), node_color='#7A83AC', node_size=30, alpha=0.5)
  nx.draw_networkx_nodes(g, pos=pos, ax=axs, nodelist=list(df['trg'].values), node_color='k', node_size=20, alpha=0.8)

  axs.patch.set_facecolor('None')
  axs.set_xticks([]) #[None]# grid(True, which='both')
  axs.set_yticks([]) #[None]# grid(True, which='both')
  plt.savefig('figures/outfig', bbox_inches='tight', pad_inches=0)

  return

def convert_follower_network_2edgelist():
  dbg = False
  df = pd.read_csv('Results/twtrs_follower_network.tsv', sep='\t', header=None)

  edges = []
  with open('Results/procjson.tsv', 'w') as fout:
    for row in df.iterrows():
      # get a count of the followers : a naive approach 
      users_flist = np.array([long(x) for x in row[1][1].lstrip('[').rstrip(']').split(',') if x != ''])
      sampsize = int(math.ceil(len(users_flist) * .05))
      # pick 10% of their follower network at random
      if len(users_flist) > 1:
        idx = np.arange(len(users_flist))
        np.random.shuffle(idx)
        subsample = users_flist[idx[:sampsize]]
      else:
        subsample = users_flist

      # now get the network for submample
      for j, trg in enumerate(subsample):
        fout.write('{}\t{}\n'.format(row[1][0], trg))  # ong(trg.strip())))

        edges.append((row[1][0], trg))
      if dbg:  print row[1][0], len(row[1][1].lstrip('[').rstrip(']').split(','))
    if dbg: print len(edges)
  return edges


def visualize_graph(graph):
  if graph is None: return
  G = graph
  # identify largest connected component

  Gcc = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)
  print [len(x) for x in Gcc]
  Gcc = Gcc[0]
  print nx.info(Gcc)
  print 'A'
  pos = nx.circular_layout(Gcc)
  print 'B'
  nx.draw_networkx(Gcc, pos, with_labels=False, width=0.125, node_size=20, alpha=0.5)
  # nx.draw(Gcc, pos=nx.spring_layout(G))
  # print saving to disk
  print 'Saving to disk ...'
  plt.savefig('outplot', bb__inches='tight')

  df = pd.DataFrame.from_dict(G.degree().items())
  df.columns = ['v', 'k']
  gb = df.groupby(['k']).count()
  gb['pk'] = gb / float(G.number_of_nodes())
  print gb.head(), '<= gb'
  # gb['deg'] = gb.index.values
  print gb.head()

  gb['pk'].to_csv('Results/degree.tsv', index=True, sep="\t", header=True)

  # draw graph
  # G=nx.random_geometric_graph(G.number_of_nodes(),0.125)
  # position is stored as node attribute data for random_geometric_graph
  # pos=nx.get_node_attributes(G,'pos')
  nx.draw_networkx(G, pos=nx.spring_layout(G), node_size=20, with_labels=False, alpha=0.75, weight=0.5)
  # print saving to disk
  print 'Saving to disk ...'
  plt.savefig('outplot', bb__inches='tight')


def main():
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
    edgelist = np.loadtxt(infname, dtype=str, delimiter='\t')
    print edgelist[:4]
    idx = np.arange(len(edgelist))
    np.random.shuffle(idx)
    subsamp_edgelist = edgelist[idx[:100]]
    G = nx.Graph()
    G.add_edges_from([(long(x), long(y)) for x, y in subsamp_edgelist])

  # visualize this graph
  # visualize_graph(G)
  exit()

  G = nx.Graph()
  G.add_edges_from([(long(x), long(y)) for x, y in edgelist])
  print nx.info(G)
  print 'Done'

def draw_basic_network(G):
  slpos = nx.spring_layout(G) # see this for a great grid layout [1]
  nx.draw_networkx(G, pos=slpos, node_color='b', nodelist=sourc, with_labels=False,node_size=20, \
                   edge_color='#7146CC')
  nx.draw_networkx_nodes(G, pos=slpos, node_color='r', nodelist=[x for x in g.nodes() if x not in sourc], \
                         alpha=0.8, with_labels=False,node_size=20)
  plt.savefig('figures/plotfig', bbox_inches='tight', pad_inches=0)

if __name__ == '__main__':

  if 1: draw_citing_users_follower_count()
  exit()


  infname = 'Results/procjson.tsv'
  infname = "Results/clustered_relevant_users.tsv"

  with open(infname) as f:
    lines = f.readlines()
  edges = []
  sourc = []
  for j,l in enumerate(lines):
    l = l.rstrip('\r\n')
    lparts = l.split('\t')
    edgesLst= [np.int64(p.lstrip('[').rstrip(']')) for p in lparts]
    edges.append(tuple(edgesLst))
    sourc.append(edgesLst[0])

  # Add the twitter users' follower network
  # processes this file: twtrs_follower_network.tsv
  plusEdgesLst = convert_follower_network_2edgelist()

  fllwrsEdges =[]
  for x,y in plusEdgesLst:
    x = np.int64(x)
    y = np.int64(x)
    fllwrsEdges.append((x,y))
  
  ####
  #### Builds the basic graph
  ####
  g = nx.Graph()
  g.add_edges_from(edges)
  
  print nx.info(g)
  draw_basic_network(g)
  g.add_edges_from(plusEdgesLst)
  print nx.info(g)

  ## \  /
  ##  \/ isualization
  # deg distrib
  snm.get_degree_dist([g],"citeplus", 'orig')

  # write to disk clustering coeffs for this graph
  snm.get_clust_coeff([g], 'orig', 'citeplus')

  # write to disk egienvalue
  snm.network_value_distribution([g], [], 'citeplus')

  if 0:
    L = nx.normalized_laplacian_matrix(g)
    e = np.linalg.eigvals(L.A)
    print("Largest eigenvalue:", max(e))
    print("Smallest eigenvalue:", min(e))
