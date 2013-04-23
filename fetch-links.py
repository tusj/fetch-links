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
parser.add_argument("-v", "--verbose", help="Increase program output", action="store_true")
parser.add_argument("-l", "--list", help="Print out a list of the URL's found", action="store_true")
parser.add_argument("--nodownload", help="Skip Downloading, implies --list option", action="store_true")

args = parser.parse_args()

t = args.include.split(" ")
tt = [ "(" + ti + ")" for ti in t ]
restring = ".*\." + "|".join(tt)
fileTypeFilter = re.compile(restring)

if not args.url.startswith("http://"):
	print "error: The URL given needs to be complete"
	os.exit(1)

def makedir(dirname):
	if not os.path.exists(dirname):
		os.makedirs(dirname)
		return True

dirname = ""
if args.directory:
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
links = soup.findAll(name='a', attrs={'href': fileTypeFilter})

def fetchLink(link):
	urllib.urlretrieve(link.get('href'), os.path.basename(link.get('href')))

if args.nodownload or args.list:
	for l in links:
		print l.get('href')
	if args.nodownload:
		sys.exit(0)


tic = time.time()
n = len(links)
nSize = len(str(n))

results = pprocess.Map(limit=min(n, maxParallelRequests))
fetchParallel = results.manage(pprocess.MakeParallel(fetchLink))

for link in links:
	fetchParallel(link)

if args.verbose:
	fish = ProgressFish(total=n)
	print
	for i, res in enumerate(results):
		fish.animate(amount=i)

	if not args.directory:
		print 'fetched {} links into directory {}\n'.format(n, dirname)
	print 'time used: {} seconds'.format(round(time.time() - tic, 2))
