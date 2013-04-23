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
parser.add_argument("-d", "--directory", help="specify a directory to store the links in")
args = parser.parse_args()

t = args.include.split(" ")
tt = [ "(" + ti + ")" for ti in t ]
restring = "|".join(tt)
regexObj = re.compile(restring)

def makedir(dirname):
	if not os.path.exists(dirname):
		print "made dir", dirname
		os.makedirs(dirname)
		return True

dirname = ""
if args.directory:
	print "directory specified: ", args.directory
	dirname = args.directory
	makedir(dirname)
else:
	dirname = os.path.basename(args.url.strip('/'))
	if not makedir(dirname):
		dirname = args.url.strip('http://')
		makedir(dirname)

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


if not args.directory:
	print 'fetched {} links into directory {}\n'.format(n, dirname)
print 'time used: {} seconds'.format(round(time.time() - tic, 2))
