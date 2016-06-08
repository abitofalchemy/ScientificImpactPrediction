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
	print type(G)
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
#   convert_follower_network_2edgelist()
	infname = 'Results/procjson.tsv'
	#   if 0:
	#   	G = nx.read_edgelist(infname)
	#   	print nx.info(G)
	edgelist= np.loadtxt(infname,dtype=str, delimiter='\t')
	print edgelist[:4]
	idx = np.arange(len(edgelist))
	np.random.shuffle(idx)
	subsamp_edgelist = edgelist[idx[:100]]
	G = nx.Graph()
	G.add_edges_from([(long(x),long(y)) for x,y in subsamp_edgelist])

	# visualize this graph 
	visualize_graph(G)
	exit()
	
	G = nx.Graph()
	G.add_edges_from([(long(x),long(y)) for x,y in edgelist])
	print nx.info(G)
	print 'Done'	
