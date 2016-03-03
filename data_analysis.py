__author__ = 'saguinag'+'@'+'nd.edu'
__version__ = "0.1.0"

##
##  data_analysis = hyperedge replacement grammars model
##

## TODO: some todo list
#

## VersionLog:
# 0.0.1 Initial commit
#

import argparse,traceback,optparse
import time, os, sys,  csv, json
import pandas as pd 
import networkx as nx

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
  parser.add_argument('json_file', metavar='JSONFILE',    help='Input File')
  parser.add_argument('--version', action='version', version=__version__)
  return parser

def paris():
  parser = get_parser()
  args = vars(parser.parse_args())
  #print args
  infile = args['json_file']
  outfile= '../NetAnalysis/' + os.path.basename(infile).split('.')[0] +'_0.edgelist'
  
  print 'Processing:',infile
  print '-'*80

  data = []
  with open(infile, 'r') as fp:
    i =0
    for l in fp.readlines():
      # objs = l.replace('}{','}}\t{{').split('}\t{')
      # tw_lst = [json.loads(obj) for obj in objs]
      l = l.rstrip() #len(l),l[-1]
      l = l.replace("None","'None'")
      l = l.replace("False","'False'")
      l = l.replace("True","'True'")
      l = l.replace("'","\"")
      print l
      print type(json.loads(str(l)))
      
      break
  return

def main():
  parser = get_parser()
  args = vars(parser.parse_args())

  #print args
  infile = args['json_file']
  outfile= '../NetAnalysis/' + os.path.basename(infile).split('.')[0] +'_0.edgelist'
  
  print 'Processing:',infile
  print '-'*80

  data = []
  with open(infile, 'r') as fp:
    i =0
    for l in fp.readlines():
      objs = l.replace('}{','}}\t{{').split('}\t{')
      tw_lst = [json.loads(obj) for obj in objs]
      #print len(tw_lst)
  '''
  print type(tw_lst[0])
  print tw_lst[0].keys()
  '''
  edge_lst = []
  #print '{0: <16}{1: <24}{2}'.format('source','claim','screen_name','posted_at') 
  for d in tw_lst:
    print '{0}\t{1}\t{2}'.format(d['user']['id'], d['id'], d['created_at']) 
    edge_lst.append((d['user']['id'], d['id'], d['created_at']))
  
  df = pd.DataFrame( edge_lst)
  print df.head()
  
  # write to disk
  if os.path.exists(outfile):
    bsnm = os.path.basename(infile).split('.')[0]
    print bsnm
    filesType =filter(lambda f: f.startswith(bsnm), [f for f in os.listdir('../NetAnalysis/') if os.path.isfile(os.path.join('../NetAnalysis/', f))])
    
    outfile= '../NetAnalysis/' + os.path.basename(infile).split('.')[0] 
    outfile += '_' + str(len(filesType)) +'.edgelist'
    print outfile
  

  of = open(outfile, 'w')
  of.write('% '+outfile.split('/')[-1] +'\n')
  of.write('% {source} {claim} {timestamp}\n')
  of.close()

  df.to_csv(outfile, mode='a', sep='\t', header=False, index=False)

if __name__ == '__main__':

  # main()
  paris()
  print 'Done.'
  sys.exit(0)

