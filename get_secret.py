#!/usr/bin/env python
'''
This is to get a refresh token from a private script app created through Reddit
apps here: https://www.reddit.com/prefs/apps/

1. Create app at above URI, using the private script option
2. Enter client_id and secret into praw.ini
3. Run this script
4. At the prompt copy the URL and open it in your browser. Allow access to your
private app and it'll redirect you to a broken webpage.
5. Copy the code printed into your console as the oauth_refresh_token and enter
t in praw.ini
6. All future requests through praw will use praw.ini to login with OAuth2

Once client/secret/refresh are in praw.ini you only have to call
refresh_access_information() instead of get_authorize_url() ->
get_access_information().
'''

import praw
from praw.errors import HTTPException
from tornado import gen, web
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

r = praw.Reddit('Shreddit refresh token grabber')


class Page(web.RequestHandler):
    def get(self):
        code = self.get_argument("code", default=None, strip=False)
        self.write("Success! Your code: %s" % code)
        IOLoop.current().stop()
        self.login(code)

    def login(self, code):
        deets = r.get_access_information(code)
        print("oauth_refresh_token (put in praw.ini): %s" % deets['refresh_token'])
        r.set_access_credentials(**deets)
        # TODO: Automatically update praw.ini with refresh_token

application = web.Application([
    (r"/authorize_callback", Page),
])

try:
    r.refresh_access_information()
except HTTPException:
    url = r.get_authorize_url('uniqueKey', ['identity', 'read', 'vote', 'edit',
        'history'], True)
    print("Please open: ", url)
    server = HTTPServer(application)
    server.listen(65010)
    IOLoop.current().start()

if r.user == None:
    print("Failed to log in. Something went wrong!")
else:
    print("Logged in as %s." % r.user)

print()

