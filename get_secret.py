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
import webbrowser
from warnings import warn
from praw.errors import HTTPException, OAuthAppRequired
from tornado import gen, web
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

r = praw.Reddit('Shreddit refresh token grabber')


class Page(web.RequestHandler):
    def get(self):
        code = self.get_argument("code", default=None, strip=False)
        self.write("Success! Your code: %s<br> \
        It will now be appended to praw.ini and you \
                should be able to enjoy Shreddit without storing \
                your user / pass anywhere." % code)
        IOLoop.current().stop()
        self.login(code)

    def login(self, code):
        deets = r.get_access_information(code)
        print("oauth_refresh_token: %s" % deets['refresh_token'])
        r.set_access_credentials(**deets)
        with open('praw.ini', mode='a') as fh:
            fh.write('oauth_refresh_token = %s' % deets['refresh_token'])
            print("Refresh token written to praw.ini")

application = web.Application([(r"/", Page)])

try:
    r.refresh_access_information()
except HTTPException:
    url = r.get_authorize_url('uniqueKey', ['identity', 'read', 'vote', 'edit', 'history'], True)
    try:
        webbrowser.open(url, new=2)
    except NameError:
        warn('''Couldn't open URL: %s\n please do so manually''' % url)
    server = HTTPServer(application)
    server.listen(65010)
    IOLoop.current().start()

if r.user == None:
    print("Failed to log in. Something went wrong!")
else:
    print("Logged in as %s." % r.user)

print()

