#!/usr/bin/env python2

import sys
try: import json
except ImportError: import simplejson as json
from urllib2 import urlopen, HTTPError
from time import sleep

f = open('user.json', 'r')
user = json.load(f)['user']
f.close()

sub_section = 'comments'
after = ''

init_url = 'http://www.reddit.com/user/{user}/comments/.json?after=%s'.format(user=user)
next_url = init_url % after

http = urlopen(next_url)
reddit = json.load(http)

datum = []
while True:
    after = reddit['data']['after']
    children = reddit['data']['children']

    # This bit fills datum with the id (for removal) and the date (for saving recent posts)
    for child in children:
        child_data = child['data']
        if 'id' in child_data:
            datum.append({
                'id': child_data[u'name'],
                'created': child_data['created'],
                'body': child_data['body'],
                'subreddit': child_data['subreddit']})

    if after == None:
        break

    next_url = init_url % after
    http = urlopen(next_url)
    reddit = json.load(http)
    sleep(1)

f = open('data.json', 'w')
json.dump(datum, f)
f.close()
