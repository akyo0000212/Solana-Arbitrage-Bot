#!/usr/bin/env python2

try: import json
except ImportError: import simplejson as json
import sys, httplib, urllib
from datetime import datetime, timedelta
from time import sleep

## Get the data we need to log into the API
f = open('user.json', 'r')
data = json.load(f)
f.close()

days = data['days']
user = data['user']
passwd = data['passwd']

## Load our json which should be all the user's history
f = open('data.json', 'r')
data = json.load(f)
f.close()

# Every thing before this time will be deleted
before_time = datetime.now() - timedelta(days=days)

## Fill an array of IDs that are to be deleted
deletion_ids = []
for d in data:
    date = datetime.fromtimestamp(d['created'])
    if date < before_time:
        deletion_ids.append(d)

if len(deletion_ids) == 0:
    print "Couldn't find any posts to delete"
    exit(0)


## This part logs you in.
headers = {
    "Content-type": "application/x-www-form-urlencoded",
    "User-Agent": "Shreddit"
    }
conn = httplib.HTTPSConnection('ssl.reddit.com')
params = urllib.urlencode({
    'user': user,
    'passwd': passwd,
    'api_type': 'json'})

conn.request("POST", "/api/login/%s" % user, params, headers)
http = conn.getresponse()
tmp = json.loads(http.read())['json']['data']
headers.update({'Cookie': 'reddit_session=%s' % tmp['cookie']})
modhash = tmp['modhash']

for dat in deletion_ids:
    id = dat['id']
    time = datetime.fromtimestamp(dat['created']).date()
    subreddit = dat['subreddit']
    text = dat[u'body'][:20]

    #print '{id}: {time} {subreddit}: "{text}..."'.format(subreddit=subreddit, id=id, time=time, text=text)
    # And now for the deleting
    conn = httplib.HTTPConnection('www.reddit.com')
    params = urllib.urlencode({
        'id': id,
        'uh': modhash,
        'api_type': 'json'})
    #headers.update({"Content-Length": len(params)})
    conn.request('POST', '/api/del', params, headers)
    http = conn.getresponse()
    if http.read() != '{}':
        print '''Failed to delete "%s" (%s - %s - %s)''' % (text, id, time, subreddit)
    sleep(2)
