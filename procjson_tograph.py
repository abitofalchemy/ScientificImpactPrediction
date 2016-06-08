import shelve
import numpy as np 
import pandas as pd
import networkx as nx
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
			for j, trg in enumerate(row[1][1].lstrip('[').rstrip(']').split(',')):
				fout.write('{}\t{}\n'.format(row[1][0], long(trg.strip())))
				
				edges.append((row[1][0], trg[0]))
			if dbg:  print row[1][0], len(row[1][1].lstrip('[').rstrip(']').split(','))
		if dbg: print len(edges)
			
			
	
	return edges
	

def visualize_graph(graph):
	if graph is None:	return
	G  = graph
	df = pd.DataFrame.from_dict(G.degree().items())
	df.columns =['v','k']
	gb = df.groupby(['k']).count()
	gb['pk'] = gb/float(G.number_of_nodes())
	print gb.head(), '<= gb'
	
  # draw graph
	G=nx.random_geometric_graph(G.number_of_nodes(),0.125)
	# position is stored as node attribute data for random_geometric_graph
	pos=nx.get_node_attributes(G,'pos')
	nx.draw_networkx(G, pos=pos, node_size=20, with_labels=False,  alpha=0.75)
	# print saving to disk
	print 'Saving to disk ...'
	plt.savefig('outplot',bb__inches='tight')
	
if __name__ == '__main__':
#   convert_follower_network_2edgelist()
  
  infname = 'Results/procjson.tsv'
  G = nx.read_edgelist(infname)
  print nx.info(G)

	# visualize this graph 
  visualize_graph(G)
