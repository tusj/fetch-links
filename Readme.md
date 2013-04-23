Fetch-links
===========

A small python script which can find and download all links from a website

Usage
-----
```
./fetch-links.py -h
usage: fetch-links.py [-h] [-d DIRECTORY] [-v] [-l] [--nodownload] url include

positional arguments:
  url                   Fetches all links from url given
  include               list include patterns here Example: include pdf:
                        .*\.pdf

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        specify a directory to store the links in
  -v, --verbose         Increase program output
  -l, --list            Print out a list of the URL's found
  --nodownload          Skip Downloading, implies --list option
```