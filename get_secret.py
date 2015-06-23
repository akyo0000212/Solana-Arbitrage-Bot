#!/usr/bin/env python
'''
This is to get a refresh token from a private script app created through Reddit
apps here: https://www.reddit.com/prefs/apps/

1. Create app at above URI, using the private script option
2. Enter client_id and secret into praw.ini
3. Run this script
4. At the prompt copy the URL and open it in your browser. Allow access to your
private app and it'll redirect you to a broken webpage.
5. Copy the &secret=abc123 into refresh_token in praw.ini

Once client/secret/refresh are in praw.ini you only have to call
refresh_access_information() instead of get_authorize_url() ->
get_access_information().
'''

import praw
from praw.errors import HTTPException
r = praw.Reddit('Shreddit refresh token grabber')

try:
    r.refresh_access_information()
except HTTPException:
    url = r.get_authorize_url('uniqueKey', 'identity', True)
    print("Please open: ", url)
    access_key = input("Enter your access key (secret param): ")
    deets = r.get_access_information(access_key)
    print("oauth_refresh_token (put in praw.ini): %s" % deets['refresh_token'])
    r.set_access_credentials(**deets)

if r.user == None:
    print("Failed to log in. Something went wrong!")
else:
    print("Logged in as %s.\n" % r.user)

