#!/usr/bin/env python2

import sys
from json import loads, dumps
from urllib2 import urlopen
from time import sleep

if len(sys.argv) != 2:
    raise Exception("You must specifiy a user")

user = sys.argv[1]

sub_section = 'comments'
after = ''

init_url = 'http://www.reddit.com/user/{user}/comments/.json?after=%s'.format(user=user)
next_url = init_url % after

http = urlopen(next_url).read()
json = loads(http)

datum = []
while True:
    print "Grabing IDs for after: ", after
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
    sleep(2) # don't want to hammer reddit to hard

print "Script collected all available data."

f = open('data.json', 'w')
f.write(dumps(datum))
f.close()
