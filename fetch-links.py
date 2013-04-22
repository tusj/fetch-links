#!/usr/bin/python
# Fetches data files from given link as argument.
# TODO: Parallelize and make recursive. Currently
# skips subdirectories. Also increase robustness.
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import re
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
dirname = os.path.basename(urlname.strip('/'))

if not os.path.exists(dirname):
	os.mkdir(dirname)
else:
	dirname = urlname
	if not os.path.exists(dirname):
		os.makedirs(dirname)

os.chdir(dirname)
html_page = urllib2.urlopen(urlname)
soup = BeautifulSoup(html_page)
links = soup.findAll('a')

def fetchLink(link):
	urllib.urlretrieve(urlname + link.get('href'), link.get('href'))

limit = len(links)
#results = pprocess.pmap(fetchLink, links, limit=limit)
i = 0
n = len(links)

tic = time.time()
for link in links:
	if str(link.get('href'))[-1] == '/':
		continue
	print "fetching #", i, " of ", n, ": ", link.get('href')
	fetchLink(link)
	i += 1


print "fetched ", len(links), " into directory ", dirname
print "time used:", time.time() - tic, "seconds"

