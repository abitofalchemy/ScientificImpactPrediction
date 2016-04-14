# -*- coding: utf-8 -*-

__author__ = "Sal Aguinaga"
__copyright__ = "Copyright 2015, The Phoenix Project"
__credits__ = ["Sal Aguinaga", "Rodrigo Palacios", "Tim Weninger"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Sal Aguinaga"
__email__ = "saguinag (at) nd dot edu"

import json
import argparse,traceback
from pprint import pprint


def parse_input_args():
  parser = argparse.ArgumentParser(description='query twitter and output to file')
  parser.add_argument('injson', metavar='INJSON', help='Input JSON path')
  parser.add_argument('--version', action='version', version=__version__)
  args = vars(parser.parse_args())
  return args


# << Begin >>

args = parse_input_args()
in_json_path   = args['injson']

# reads in the JSON file
json_data = []
docsd  = {}
with open(in_json_path) as f:
  for line in f:
    jobj=json.loads(line)
    json_data.append(jobj)

# for jl in json_data:
#   print jl['details_url']
#   for alt_k in jl.keys():
    
#     #if 'count_inprint '{}\t: {}\n'.format(alt_k, jl[alt_k])
#     if 'count' in alt_k:  
#       print '\t',alt_k, jl[alt_k]
  for jl in json_data:
    packet_ar = []
    for ak in jl.keys():
      # print [x for x in str(ak)]
      if '_id' in ak:   packet_ar.append(jl[ak])
      if 'count' in ak: packet_ar.append(jl[ak])
    print packet_ar

print '-'*80

alt_pub = json_data[-1]
pprint(alt_pub.keys())
pub_title = 'Publication title: {}'.format(alt_pub['title'])
print pub_title
print alt_pub['cited_by_tweeters_count']
## counts 
'''
for ak in jl.keys():
# print [x for x in str(ak)]
  if '_id' in ak:   packet_ar.append(jl[ak])
  if 'count' in ak: packet_ar.append(jl[ak])count_ar = 
'''
cnt_d = {}
for k,v in alt_pub.items():
  if 'count' in k:
    cnt_d[k] = v

pprint(cnt_d)

print '-'*80
pprint(alt_pub['tq'])


####
