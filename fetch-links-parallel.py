#!/usr/bin/python
# Fetches data files from given link as argument.
# TODO: increase robustness.
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import sys
import os.path
import os
import pprocess
import time

if len(sys.argv) != 2:
	print "Fetches all links from url given"
	print "Usage: ", sys.argv[0], " url"
	exit(1)

urlname = sys.argv[1]
if urlname[-1] != '/':
	urlname = urlname + '/'

dirname = os.path.basename(urlname.strip('/'))

if not os.path.exists(dirname):
	os.mkdir(dirname)
else:
	dirname = urlname
	if not os.path.exists(dirname):
		os.makedirs(dirname)

os.chdir(dirname)

def findLinks(urlname):
	html_page = urllib2.urlopen(urlname)
	soup = BeautifulSoup(html_page)
	return soup.findAll('a')

def fetchLink(link):
	urllib.urlretrieve(urlname + link, link)
	return link

def fetchLinks(links):
	cntLinks = 0
	for l in links:
		fileName = l.get('href')
		if str(fileName)[-1] == '/':
			if str(fileName)[0] == '/':
				continue
			if urlname[-1] == '/':
				newURL = urlname[:-1] + fileName
			else:
				newURL = urlname + fileName
			print newURL
			newLinks = findLinks(newURL)
			cntLinks += fetchLinks(newLinks)
			continue
		calc(fileName)
		cntLinks += 1
	return cntLinks

links = findLinks(urlname)
limit = len(links) 
results = pprocess.Map(limit=limit)
calc = results.manage(pprocess.MakeParallel(fetchLink))
cntLinks = fetchLinks(links)

print "fetching", cntLinks, "files from", urlname, "..."
print

tic = time.time()
i = 1
for result in results:
	print str(i) + ":\t", result
	i += 1

print
print "fetched", len(links), "urls into directory", dirname
print
print "time used:", time.time() - tic, "seconds"
