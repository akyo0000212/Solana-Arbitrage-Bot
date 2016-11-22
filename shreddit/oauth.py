"""This module contains a function that tests OAuth session validity.
"""
import os
import praw


def oauth_test(praw_ini):
    if praw_ini:
        # PRAW won't panic if the file is invalid, so check first
        if not os.path.exists(praw_ini):
            print("PRAW configuration file \"{}\" not found.".format(praw_ini))
            return
        praw.settings.CONFIG.read(praw_ini)
    r = praw.Reddit("Shreddit oauth test")
    try:
        r.refresh_access_information()
        if r.is_oauth_session():
            print("Session is valid.")
        else:
            print("Session is not a valid OAuth session.")
    except Exception as e:
        print("Error encountered while checking credentials:\n{}".format(e))
