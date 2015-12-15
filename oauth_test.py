#!/usr/bin/env python
'''
Simple script to check if your oauth is working.
'''
import praw
import sys

r = praw.Reddit('Shreddit oauth test')
try:
    r.refresh_access_information()
    if r.is_oauth_session():
        sys.exit(0)
    else:
        sys.exit(2)
except:
    sys.exit(1)

