from pattern.web import URL, plaintext, download
import numpy as np
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import pandas as pd
import socket

# from urllib.request import urlopen
# import urllib
# import HTMLParser

fname = 'Results/tweets_hyperlinks.tsv'
lns = np.loadtxt(fname, dtype=str, unpack=True)
# engine = Google(license=None) # Enter your license key.
# for result in engine.search(url)
# 	print result.url
# >>>     print result.text
# engine = Bing(license=None)
url_title = {}
title =""
for j,mUrl in enumerate(lns):
	#mUrl =str('https://t.co/XtkITIcIUu')
  print j
  try:
    url = BeautifulSoup(urllib2.urlopen(mUrl, timeout=1))
    if  url.title:
      title = url.title.string
  except socket.error as socketerror:
		print("Error: ", socketerror)
		pass
  except urllib2.HTTPError, e:
    url = URL(mUrl)
    if 'link' in url.headers.keys():
        s = url.headers['link']
        #print [x for x in re.search("(?P<url>https?://[^\s]+)", s).group("url") if "p=" in x]
        title = [x.strip(';').strip('>') for x in re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', s) if "p=" in x]#.strip(';').strip('>')		
  except urllib2.URLError, e:
    url = URL(mUrl)
    if url.headers:
			s = url.headers['link']
			title = [x.strip(';').strip('>') for x in re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', s) if "p=" in x]#.strip(';').strip('>')
# 	except socket.timeout, e:
# 		title = ""
# 		pass
	
  url_title[mUrl] = title

print len(url_title)
df = pd.DataFrame.from_dict(url_title.items())
print df.head()
df.to_csv("Results/hlinks_titles.tsv", sep="\t")

	# s = url.download()
# 	s = plaintext(s, keep={'title':[]})
# 	print s.find(".//title").text
#	print url.headers['link']
	
	
	
	
exit(0)	
# 	print str( urllib.request.urlopen(url).read())
# 	break
# # 	print  extension(url.page)
# # 	print url.string
# # 	print url.parts
# 	for result in Newsfeed().search(url):
# 		print repr(result.title)
# 	break


# 	response = urllib2.urlopen(url)
# 	soup = BeautifulSoup(response.read(), from_encoding=response.info().getparam('charset'))
# 	title = soup.find('title').text
# 	response = urllib2.urlopen(url)
# 	html = response.read()
# 	soup = BeautifulSoup(html)
# 	print title
# 	break
