Fetch-links
===========

A small python script which can find and download all links from a website

Usage
-----
```
usage: fetch-links.py [-h] [-i INCLUDE] [-r] [-d DIRECTORY] [-v] [-l] [-n] url

positional arguments:
  url                   Fetches all links from url given

optional arguments:
  -h, --help            show this help message and exit
  -i INCLUDE, --include INCLUDE
                        List include patterns here Example: include pdf and
                        doc: "pdf doc"
  -r, --regex           Specify include pattern as regular expression
                        according to Python syntax Example: include everything
                        which contains hello: ".*hello.*"
  -d DIRECTORY, --directory DIRECTORY
                        Specify a directory to store the links in
  -v, --verbose         Increase program output
  -l, --list            Print out a list of the URL's found
  -n, --nodownload      Skip Downloading, implies --list option

```
