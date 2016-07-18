import os
import sys
import logging
import argparse
import json
import arrow
import yaml
import praw
import time
from re import sub
from datetime import datetime, timedelta
from praw.errors import (InvalidUser, InvalidUserPass, RateLimitExceeded, HTTPException, OAuthAppRequired)
from praw.objects import Comment, Submission
from shreddit.util import get_sentence


class Shredder(object):
    """This class stores state for configuration, API objects, logging, etc. It exposes a shred() method that
    application code can call to start it.
    """
    def __init__(self, config, praw_ini=None):
        logging.basicConfig()
        self._logger = logging.getLogger("shreddit")
        self._logger.setLevel(level=logging.DEBUG if config.get("verbose", True) else logging.INFO)
        self._logger.info(config)

        self._praw_ini = praw_ini
        self._username, self._password = config["username"], config["password"]
        self._connect(praw_ini, self._username, self._password)

        if config.get("save_directory", "."):
            self._r.config.store_json_result = True

        # Read some information from the config and store it
        # TODO: Handle this in a much cleaner way
        self._whitelist = set(config.get("whitelist", []))
        self._whitelist_ids = set(config.get("whitelist_ids", []))
        self._item = config.get("item", "comments")
        self._sort = config.get("sort", "new")
        self._whitelist_dist = config.get("whitelist_distinguished", False)
        self._whitelist_gild = config.get("whitelist_gilded", False)
        self._max_score = config.get("max_score", None)
        self._recent_cutoff = arrow.now().replace(hours=-config.get("hours", 24))
        self._nuke_cutoff = arrow.now().replace(hours=-config.get("nuke_hours", 4320))
        self._save = config.get("save_directory", None)
        self._trial = config.get("trial_run", False)
        self._clear_vote = config.get("clear_vote", False)
        self._repl_format = config.get("replacement_format")
        self._edit_only = config.get("edit_only", False)
        self._batch_cooldown = config.get("batch_cooldown", 10)
        if self._save:
            if not os.path.exists(self._save):
                os.makedirs(self._save)
        self._limit = None
        self._logger.info("Deleting ALL items before {}".format(self._nuke_cutoff))
        self._logger.info("Deleting items not whitelisted until {}".format(self._recent_cutoff))
        self._logger.info("Ignoring ALL items after {}".format(self._recent_cutoff))
        self._logger.info("Targeting {} sorted by {}".format(self._item, self._sort))
        if self._whitelist:
            self._logger.info("Keeping items from subreddits {}".format(", ".join(self._whitelist)))
        if self._save:
            self._logger.info("Saving deleted items to: {}".format(self._save))
        if self._trial:
            self._logger.info("Trial run - no deletion will be performed")

    def shred(self):
        deleted = self._remove_things(self._get_things())
        if deleted >= 1000:
            # This user has more than 1000 items to handle, which angers the gods of the Reddit API. So chill for a
            # while and do it again.
            self._logger.info("Finished deleting 1000 items. " \
                              "Waiting {} seconds and continuing...".format(self._batch_cooldown))
            time.sleep(self._batch_cooldown)
            self._connect(None, self._username, self._password)
            self.shred()

    def _connect(self, praw_ini, username, password):
        self._r = praw.Reddit(user_agent="shreddit/4.2")
        if praw_ini:
            # PRAW won't panic if the file is invalid, so check first
            if not os.path.exists(praw_ini):
                print("PRAW configuration file \"{}\" not found.".format(praw_ini))
                return
            praw.settings.CONFIG.read(praw_ini)
        try:
            # Try to login with OAuth2
            self._r.refresh_access_information()
            self._logger.debug("Logged in with OAuth.")
        except (HTTPException, OAuthAppRequired) as e:
            self._logger.warning("You should migrate to OAuth2 using get_secret.py before Reddit disables this login "
                                 "method.")
            try:
                try:
                    self._r.login(username, password)
                except InvalidUserPass:
                    self._r.login()  # Supply details on the command line
            except InvalidUser as e:
                raise InvalidUser("User does not exist.", e)
            except InvalidUserPass as e:
                raise InvalidUserPass("Specified an incorrect password.", e)
            except RateLimitExceeded as e:
                raise RateLimitExceeded("You're doing that too much.", e)
        self._logger.info("Logged in as {user}.".format(user=self._r.user))

    def _check_item(self, item):
        """Returns True if the item is whitelisted, False otherwise.
        """
        if str(item.subreddit).lower() in self._whitelist or item.id in self._whitelist_ids:
            return True
        if self._whitelist_dist and item.distinguished:
            return True
        if self._whitelist_gild and item.gilded:
            return True
        if self._max_score is not None and item.score > self._max_score:
            return True
        return False

    def _save_item(self, item):
        with open(os.path.join(self._save, item.id), "w") as fh:
            json.dump(item.json_dict, fh)

    def _remove_submission(self, sub):
        self._logger.info("Deleting submission: #{id} {url}".format(id=sub.id, url=sub.url.encode("utf-8")))

    def _remove_comment(self, comment):
        if self._repl_format == "random":
            replacement_text = get_sentence()
        elif self._repl_format == "dot":
            replacement_text = "."
        else:
            replacement_text = self._repl_format

        short_text = sub(b"\n\r\t", " ", comment.body[:35].encode("utf-8"))
        msg = "/r/{}/ #{} ({}) with: {}".format(comment.subreddit, comment.id, short_text, replacement_text)
            
        if self._edit_only:
            self._logger.info("Editing (not removing) {msg}".format(msg=msg))
        else:
            self._logger.info("Editing and deleting {msg}".format(msg=msg))
        if not self._trial:
            comment.edit(replacement_text)

    def _remove(self, item):
        if self._save:
            self._save_item(item)
        if self._clear_vote:
            item.clear_vote()
        if isinstance(item, Submission):
            self._remove_submission(item)
        elif isinstance(item, Comment):
            self._remove_comment(item)
        if not self._edit_only and not self._trial:
            item.delete()

    def _remove_things(self, items):
        for idx, item in enumerate(items):
            self._logger.debug("Examining: {}".format(item))
            created = arrow.get(item.created_utc)
            if created <= self._nuke_cutoff:
                self._logger.debug("Item occurs prior to nuke cutoff")
                self._remove(item)
            elif created > self._recent_cutoff:
                self._logger.debug("Skipping due to: too recent")
                continue
            elif self._check_item(item):
                self._logger.debug("Skipping due to: whitelisted")
                continue
            else:
                self._remove(item)
            if not idx % 10:
                self._logger.info("{} items handled.".format(idx + 1))
        return idx + 1

    def _get_things(self):
        if self._item == "comments":
            return self._r.user.get_comments(limit=self._limit, sort=self._sort)
        elif self._item == "submitted":
            return self._r.user.get_submitted(limit=self._limit, sort=self._sort)
        elif self._item == "overview":
            return self._r.user.get_overview(limit=self._limit, sort=self._sort)
        else:
            raise Exception("Your deletion section is wrong")
