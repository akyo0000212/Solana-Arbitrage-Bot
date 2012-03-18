#!/usr/bin/env python2

import sys
from json import loads, dumps
from urllib2 import urlopen, HTTPError
from time import sleep

user = None
if len(sys.argv) == 2:
    user = sys.argv[1]
else:
    f = open('user.json', 'r')
    user = loads(f.read())['user']
    f.close()

sub_section = 'comments'
after = ''

init_url = 'http://www.reddit.com/user/{user}/comments/.json?after=%s'.format(user=user)
next_url = init_url % after

try:
    http = urlopen(next_url).read()
except HTTPError:
    raise HTTPError("You seem to have given an invalid user")

try:
    json = loads(http)
except ValueError:
    raise ValueError("Failed to decode json.")

datum = []
while True:
    after = json['data']['after']
    children = json['data']['children']

    # This bit fills datum with the id (for removal) and the date (for saving recent posts)
    for child in children:
        child_data = child['data']
        if 'id' in child_data:
            datum.append({'id': child_data[u'id'], 'date': child_data['created_utc']})

    if after == None:
        break

    next_url = init_url % after
    http = urlopen(next_url).read()
    json = loads(http)
    sleep(1) # don't want to hammer reddit to hard

f = open('data.json', 'w')
f.write(dumps(datum))
f.close()
