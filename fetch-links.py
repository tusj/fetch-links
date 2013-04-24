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
parser.add_argument("-i", "--include", help="List include patterns here\nExample: include pdf and doc: \"pdf doc\"")
parser.add_argument("-r", "--regex", help="Specify include pattern as regular expression according to Python syntax\nExample: include everything which contains hello: \".*hello.*\"", action="store_true")
parser.add_argument("-d", "--directory", help="Specify a directory to store the links in")
parser.add_argument("-v", "--verbose", help="Increase program output", action="store_true")
parser.add_argument("-l", "--list", help="Print out a list of the URL's found", action="store_true")
parser.add_argument("-n", "--nodownload", help="Skip Downloading, implies --list option", action="store_true")

args = parser.parse_args()

restring = ".+\..+"
if args.include:
	t = args.include.split(" ")
	restring = ".+\.(" + "|".join(t) + ")"
if args.regex:
	restring = args.include
try:
	fileTypeFilter = re.compile(restring)
except re.error as e:
	print "Error for regular expression \"{}\": {}".format(restring, e.message)
	sys.exit(1)

if not args.url.startswith("http://"):
	print "error: The URL given needs to be complete"
	sys.exit(1)

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
	l = link.get('href')
	if l == os.path.basename(l):
		l = args.url
	fileName = urllib2.unquote(os.path.basename(link.get('href')))
	urllib.urlretrieve(l, fileName)

if args.nodownload or args.list or args.verbose:
	ordnum = 15
	for l in links:
		print urllib2.unquote(l.get('href'))
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
		fish.animate(amount=i+1)

	if not args.directory:
		print 'fetched {} links into directory {}\n'.format(n, dirname)
	print 'time used: {} seconds'.format(round(time.time() - tic, 2))
