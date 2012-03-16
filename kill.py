#!/usr/bin/env python2

from datetime import datetime, timedelta
from json import loads
import sys

if len(sys.argv) < 2:
    raise Exception("Need an amount of keep-days of which to save your comments.")

days = int(sys.argv[1])

before_time = datetime.now() - timedelta(days=days)

f = open('data.json', 'r')
data = loads(f.read())
f.close()

for d in data:
    date = datetime.fromtimestamp(d['date'])
    if date < before_time:
        delete_post(d['id'])
