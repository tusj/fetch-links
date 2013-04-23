#!/usr/bin/python
# Fetches data files from given link as argument.
# TODO: Add test for url check.
# Currently skips subdirectories.

from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import sys
import os.path
import os
import pprocess
import time
import argparse

import re
from fish import ProgressFish

maxParallelRequests = 24


parser = argparse.ArgumentParser()
parser.add_argument("url", help="Fetches all links from url given")
parser.add_argument("include", help="list include patterns here\nExample: include pdf: .*\.pdf")
args = parser.parse_args()

t = args.include.split(" ")
tt = [ "(" + ti + ")" for ti in t ]
restring = "|".join(tt)
regexObj = re.compile(restring)

dirname = os.path.basename(args.url.strip('/'))
if not os.path.exists(dirname):
	os.mkdir(dirname)
else:
	dirname = args.url.strip('http://')
	if not os.path.exists(dirname):
		os.makedirs(dirname)

os.chdir(dirname)
html_page = urllib2.urlopen(args.url)
soup = BeautifulSoup(html_page)
links = soup.findAll(name='a', attrs={'href': regexObj})

def fetchLink(link):
	urllib.urlretrieve(link.get('href'), os.path.basename(link.get('href')))

tic = time.time()
n = len(links)
nSize = len(str(n))

results = pprocess.Map(limit=min(n, maxParallelRequests))
fetchParallel = results.manage(pprocess.MakeParallel(fetchLink))

for link in links:
	l = link.get('href')
	#sys.stdout.write("\n{}: of {}:\t{}\r\r\r".format(str(i).zfill(nSize), n, os.path.basename(link.get('href'))))
	#sys.stdout.flush()
	if str(l)[-1] == '/':
		continue
	fetchParallel(link)


fish = ProgressFish(total=n)
for i, res in enumerate(results):
	fish.animate(amount=i)


print 'fetched {} links into directory {}\n'.format(n, dirname)
print 'time used: {} seconds'.format(round(time.time() - tic, 2))
