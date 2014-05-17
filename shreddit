#!/usr/bin/env python2

import praw, argparse, ConfigParser
from praw.objects import Comment, Submission
from datetime import datetime, timedelta
from re import sub
from time import sleep

try:
    from loremipsum import get_sentence
except:
    get_sentence = lambda: '''I have been Shreddited for privacy!\n\nhttps://github.com/x89/Shreddit/'''

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', help="config file to use instead of shreddit.cfg")
args = parser.parse_args()

config = ConfigParser.RawConfigParser()
if args.config:
    config.read(args.config)
else:
    config.read('shreddit.cfg')

hours = config.getint('main', 'hours')
whitelist = config.get('main', 'whitelist')
whitelist_ids = config.get('main', 'whitelist_ids')
sort = config.get('main', 'sort')
verbose = config.getboolean('main', 'verbose')
clear_vote = config.getboolean('main', 'clear_vote')
trial_run = config.getboolean('main', 'trial_run')
edit_only = config.getboolean('main', 'edit_only')
item = config.get('main', 'item')

_user = config.get('main', 'username')
_pass = config.get('main', 'password')

r = praw.Reddit(user_agent="Shreddit-PRAW 2.1")

if _user and _pass:
    try:
        r.login(_user, _pass)
    except:
        # Try again (often get HTTP when Reddit is down for a second errors)
        sleep(10)
        r.login(_user, _pass)
else:
    r.login()

if verbose:
    print "Logged in as {0}".format(r.user)

if verbose:
    print "Deleting messages before {0}.".format(datetime.now() - timedelta(hours=hours))

whitelist = [y.strip().lower() for y in whitelist.split(',')]
whitelist_ids = [y.strip().lower() for y in whitelist_ids.split(',')]

if verbose:
    print "Keeping messages from subreddits {0}".format(', '.join(whitelist))

things = []
if item == "comments":
    things = r.user.get_comments(limit=None, sort=sort)
elif item == "submitted":
    things = r.user.get_submitted(limit=None, sort=sort)
elif item == "overview":
    things = r.user.get_overview(limit=None, sort=sort)
else:
    raise Exception("Your deletion section is wrong")
	
for thing in things:
    thing_time = datetime.fromtimestamp(thing.created_utc)
    # Delete things after after_time
    after_time = datetime.utcnow() - timedelta(hours=hours)
    if thing_time > after_time:
        continue
    
    # For edit_only we're assuming that the hours aren't altered.
    # This saves time when deleting (you don't edit already edited posts).
    if edit_only:
        end_time = after_time - timedelta(hours=hours)
        if thing_time < end_time:
                continue

    if str(thing.subreddit).lower() in whitelist or \
       thing.id in whitelist_ids:
        continue

    if not trial_run:
        if clear_vote:
            thing.clear_vote()
        if isinstance(thing, Submission):
            if verbose:
                print u'Deleting submission: #{0} {1}'.format(thing.id, thing.url)
        elif isinstance(thing, Comment):
            replacement_text = get_sentence()
            if verbose:
                msg = '/r/{3}/ #{0} with:\n\t"{1}" to\n\t"{2}"'.format(
                    thing.id,
                    sub(r'[\t\r\n]', ' ', thing.body.encode('ascii', 'ignore')[:78]),
                    replacement_text[:78],
                    thing.subreddit
                )
            if edit_only:
                print 'Editing ' + msg
            else:
                print 'Editing and deleting ' + msg
            thing.edit(replacement_text)
        if not edit_only:
            thing.delete()
