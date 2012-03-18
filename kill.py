#!/usr/bin/env python2

from __future__ import with_statement
try: import json
except ImportError: import simplejson as json
import sys, httplib, urllib
from datetime import datetime, timedelta
from time import sleep

## Get the data we need to log into the API
with open('user.json', 'r') as f:
    data = json.load(f)

days = data['days']
user = data['user']
passwd = data['passwd']

## Load our json which should be all the user's history
with open('data.json', 'r') as f:
    data = json.load(f)

# Every thing before this time will be deleted
before_time = datetime.now() - timedelta(days=days)

## Fill an array of IDs that are to be deleted
deletion_ids = [item for item in data if datetime.fromtimestamp(item['created']) < before_time]

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
    rid = dat['id']
    time = datetime.fromtimestamp(dat['created']).date()
    subreddit = dat['subreddit']
    text = dat[u'body'][:20]

    #print '{rid}: {time} {subreddit}: "{text}..."'.format(subreddit=subreddit, rid=rid, time=time, text=text)
    # And now for the deleting
    conn = httplib.HTTPConnection('www.reddit.com')
    params = urllib.urlencode({
        'id': rid,
        'uh': modhash,
        'api_type': 'json'})
    #headers.update({"Content-Length": len(params)})
    conn.request('POST', '/api/del', params, headers)
    http = conn.getresponse()
    if http.read() != '{}':
        print '''Failed to delete "%s" (%s - %s - %s)''' % (text, rid, time, subreddit)
    sleep(2)
