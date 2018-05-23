#!/usr/bin/python3
#Loads all csv files in a directory from the internet
#Two arguments: first argument is the url to spider, second is the directory to put the results in

import sys
import re
import urllib.request

webdir = sys.argv[1] if sys.argv[1].endswith("/") else sys.argv[1] + "/"

indexfile = urllib.request.urlopen(sys.argv[1]).read().decode('utf-8')
for pagename in re.findall('href="([^"]+\.csv)"', indexfile):
    f = open("{}/{}".format(sys.argv[2], pagename), 'w')
    f.write(urllib.request.urlopen("{}{}".format(webdir, pagename)).read().decode('utf-8'))
    f.close()
