# ScientificImpactPrediction
Using HRG model to predict scientific impact 

- PubRKD  is now the front file that can run it all.
- Need to have ..tograph take an argument to know what the hell it does and how it works
- Working on procjson.py to process the data sets and output a time series tweet count for plotting
- grep 4808504820  procjson.tsv | wc -l there should be only one; the edge list needs to be redone
 


# Links:
- http://www.clips.ua.ac.be/pattern
- [Clustering](https://wakari.io/sharing/bundle/iuliacioroianu/Text_analysis_Python_NLTK)
- [Spectral signature](http://www.sciencedirect.com/science/article/pii/S0166218X08003594)
- [Spectral Evolution](http://userpages.uni-koblenz.de/~kunegis/paper/kunegis-spectral-network-evolution.pdf)
- [Improving Twitter Retrieval by Exploiting Structural Information](http://www.aaai.org/ocs/index.php/AAAI/AAAI12/paper/view/4913)
	@inproceedings{luo2012improving,
  	title={Improving Twitter Retrieval by Exploiting Structural Information},
  	author={Luo, Zhunchen and Osborne, Miles and Wang, Ting and others},
  	booktitle={Twenty-Sixth AAAI Conference on Artificial Intelligence},
  	year={2012}
		}

# StarLog
- Proc Apollo DS
- Proc Halyard DS

- Got tweets captured > tweets processed > tweets clustered > edgelist of usr citing clust
  - i can also list usr citing tweet; 
  - [] Now I need to use the list of users and build a network from their users

- 22Mar16: Apollo DS tweets.json processed & can build a graph
  * need to add network metrics, connected components (etc.)
  * cluster tweets and plot users citing clusters & temporal signature
    - unsupervised, just give the tweets
  * build altmetric pub interest
  * develop a pub interest metric
  * HRG
  * done


