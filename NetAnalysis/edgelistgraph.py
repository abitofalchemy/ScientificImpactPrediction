#!/usr/bin/python
# encoding: utf-8
"""
catpaths

Computing the catpaths for the set of given games or actual paths

"""
__author__ = """Sal Aguinaga (saguinag@nd.edu)"""
#	Copyright (C) 2014-2015
#	Sal Aguinaga <saguinag@nd.edu>
#	All rights reserved
#	BSD license.

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##  EdgElistGraph Class
##
class EdgElistGraph():
    '''
    graphs_path Path where edgelist for ea. graph are found
    '''
    def __init__(self, graphs_path):
        self.graphs_path = graphs_path
        self.G = nx.Graph()
        self.cate = nx.Graph()
        self.page2cate = nx.Graph()

class wp_cmplx_network():
    def __init__(self, graph_path):
        self.graph_path  = graph_path
        self.graph= nx.DiGraph()
        ## Get the whole graph
        self.edge_list = []                                # stack edgelists
        with open(self.graph_path, 'rb') as f:
            inreader = csv.reader(f, delimiter='\t')    
            for row in inreader:
                self.edge_list.append(row)
        self.graph.add_edges_from(self.edge_list)

         
## http://cs224w-citation.googlecode.com/svn/trunk/networkx-community/networkx/algorithms/community/spectrum.py
def testing_networkx():
    print '-'*80+'\n',start_nodes[1], target_nodes[1]
    path_links=  nx.shortest_path(graph.netobj, start_nodes[1], target_nodes[1])
    has_path = True
    try:
        path_len = nx.shortest_path_length(graph.netobj,start_nodes[1], target_nodes[1])
    except nx.NetworkXNoPath:
        print 'No path'
        has_path = False
    if has_path:
        print start_nodes[1], target_nodes[1], path_len, path_links
    #print nx.shortest_path(graph.netobj, 788096, 14229)
    print '-'*80

def get_game_endpoints():
    filepath = "/home/saguinag/CategoryPaths/wiki_data/wpg_paths/wikipedia_games_set.tsv"
    games_set_s = pd.Series.from_csv(filepath, sep='\t', header=0)
    games_set_s.apply(str)
    return games_set_s

def read_wpg_source_target_nodes():
    src_trg_file = "wiki_data/wpg_paths/wikigame_target_nodes.txt"
    with open (src_trg_file,'rb') as f:
        lines = f.read().splitlines()
    in_table = []
    for line in lines:
        in_table.append(line.split('\t'))
    df = pd.DataFrame(in_table,columns=['src','trg'])
    return df

if __name__ == '__main__':
    from glob import glob
    import networkx as nx
    import pandas as pd
    from pprint import pprint as pp
    from os import chdir
    import csv, time
    import numpy as np
    import heapq
    from wikicatpath import get_wpg_starting_pageIds
    from wikicatpath import get_wpg_target_pageIds

    ## Hello 
    print '-'*80,'\ncatpaths\n','.'*80
    ## Establish the working directory
    chdir("/home/saguinag/CategoryPaths/")
    t0 = time.time()

    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ##  Loading end points
    ##
    if not ('wpg_endpoints_df' in globals()):
        wpg_endpoints_df = read_wpg_source_target_nodes() 
    print 'Nbr of endpoints:',np.shape(wpg_endpoints_df)
    print wpg_endpoints_df.head()
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ##  Loading the page to category graph
    ##
    if not ('page2cate' in globals()):
        page2cate = wp_cmplx_network("/home/saguinag/CategoryPaths/wiki_data/enwiki_page_to_cate.tsv")
        print ( (time.time() - t0)/60.0, 'mins wall time')
    print 'Page to Category graph loaded...'
   
    ## Test set
    #  Start and target nodes:
    #  951976   United_states
    #  36306287 Pussycat_Dolls 
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ##  Loading the Categories graph
    ## 
    t0 = time.time()
    if not ('categories' in globals()):
        categories= wp_cmplx_network("/home/saguinag/CategoryPaths/wiki_data/enwiki_cate_to_cate.tsv")
        print ( (time.time() - t0)/60.0, 'mins wall time')
    print 'Category ....... graph loaded...'

    data= []
    data.append(['u','csp','v'])
    k  = 0   # count no paths found 
    l  = 0
    output_path = "wiki_data/catpaths/" #catpaths_"+time.strftime("%d%b%y")+".txt"
    for i,row in wpg_endpoints_df.iterrows():
        if i == 0: last_u = u
        hq = []
        u = row['src']; v = row['trg']
        #print "u = row['src']; v = row['trg']", u,v
        sNodes = page2cate.graph.edges( str(u) )
        tNodes = page2cate.graph.edges( str(v) )
        c_sp = np.nan       
        #print len(sNodes),len(tNodes)
        for sp_node,sc_node in  sNodes:
            for tp_node,tc_node in tNodes:
                #print 'consider cat nodes:',sc_node, tc_node

                try:
                  c_spc = nx.shortest_path(categories.graph,
                                          str(sc_node), str(tc_node)) 
                  c_sp = len(c_spc)
                  #print 'length:', c_sp
                except nx.NetworkXNoPath as e:
                  c_sp = np.nan
                  #print '!Error:', e 
                  k = k + 1
                  pass
                heapq.heappush(hq,c_sp)
                l = l + 1
            #print k,'/', l,'no paths'
        #break
        ## u -1->sc-[]->tc-1-> v
        #print i,len(hq)
        if len(hq)>0:
            data.append([u,heapq.heappop(hq),v])
        else:
            print 'error: hq is of len:',len(hq),'nothing to pop?',i,u,v

        #print heapq.heappop(hq), k
        if not(i % 1000.): print i
        if u is not last_u:
            last_u = u
            o_file= output_path + u + "_catpaths.txt"
            np.savetxt(output_path, np.asarray(data), delimiter=',', fmt='%s')
            print 'Saved data:',u
    print 'endpoints',i,k,'/', l,'no paths'
