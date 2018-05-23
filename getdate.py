#!/usr/bin/python3
# gets the date x days ago, where x is the argument (today if no argument)
import datetime
import sys

if len(sys.argv) > 1:
    daysago = int(sys.argv[1])
else:
    daysago = 0

compdate = datetime.datetime.now() - datetime.timedelta(days=daysago)
print(compdate.strftime("%Y-%m-%d"))
