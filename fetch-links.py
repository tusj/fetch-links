#!/usr/bin/python
# Fetches data files from given link as argument.
# TODO: Currently skips subdirectories.
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import re
import sys
import os.path
import os
import pprocess
import time
import argparse
import re

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
	dirname = args.url
	if not os.path.exists(dirname):
		os.makedirs(dirname)

os.chdir(dirname)
html_page = urllib2.urlopen(args.url)
soup = BeautifulSoup(html_page)
links = soup.findAll(name='a', attrs={'href': regexObj})

def fetchLink(link):
	print args.url
	print link.get('href')
	urllib.urlretrieve(link.get('href'), os.path.basename(link.get('href')))

limit = len(links)
i = 0
n = len(links)

tic = time.time()
for link in links:
	l = link.get('href')
	if str(l)[-1] == '/':
		continue
	print "fetching #", i, " of ", n, ": ", os.path.basename(link.get('href'))
	fetchLink(link)
	i += 1


print "fetched ", len(links), " into directory ", dirname
print "time used:", time.time() - tic, "seconds"

