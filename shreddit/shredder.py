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
from praw.errors import (InvalidUser, InvalidUserPass, RateLimitExceeded,
    HTTPException, OAuthAppRequired)
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
        self.__dict__.update({"_{}".format(k): config[k] for k in config})

        self._praw_ini = praw_ini
        self._connect(praw_ini, self._username, self._password)

        if self._save_directory:
            self._r.config.store_json_result = True

        self._recent_cutoff = arrow.now().replace(hours=-self._hours)
        self._nuke_cutoff = arrow.now().replace(hours=-self._nuke_hours)
        if self._save_directory:
            if not os.path.exists(self._save_directory):
                os.makedirs(self._save_directory)
        self._limit = None
        self._api_calls = []

        # Add any multireddit subreddits to the whitelist
        self._whitelist = set([s.lower() for s in self._whitelist])
        for username, multiname in self._multi_whitelist:
            multireddit = self._r.get_multireddit(username, multiname)
            for subreddit in multireddit.subreddits:
                self._whitelist.add(str(subreddit).lower())

        # Add any multireddit subreddits to the blacklist
        self._blacklist = set()
        for username, multiname in self._multi_blacklist:
            multireddit = self._r.get_multireddit(username, multiname)
            for subreddit in multireddit.subreddits:
                self._blacklist.add(str(subreddit).lower())


        self._logger.info("Deleting ALL items before {}".format(self._nuke_cutoff))
        self._logger.info("Deleting items not whitelisted until {}".format(self._recent_cutoff))
        self._logger.info("Ignoring ALL items after {}".format(self._recent_cutoff))
        self._logger.info("Targeting {} sorted by {}".format(self._item, self._sort))
        if self._blacklist:
            self._logger.info("Deleting ALL items from subreddits {}".format(", ".join(list(self._blacklist))))
        if self._whitelist:
            self._logger.info("Keeping items from subreddits {}".format(", ".join(list(self._whitelist))))
        if self._keep_a_copy and self._save_directory:
            self._logger.info("Saving deleted items to: {}".format(self._save_directory))
        if self._trial_run:
            self._logger.info("Trial run - no deletion will be performed")

    def shred(self):
        deleted = self._remove_things(self._get_things())
        self._logger.info("Finished deleting {} items. ".format(deleted))
        if deleted >= 1000:
            # This user has more than 1000 items to handle, which angers the gods of the Reddit API. So chill for a
            # while and do it again.
            self._logger.info("Waiting {} seconds and continuing...".format(self._batch_cooldown))
            time.sleep(self._batch_cooldown)
            self._connect(None, self._username, self._password)
            self.shred()

    def _connect(self, praw_ini, username, password):
        self._r = praw.Reddit(user_agent="shreddit/5.0")
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

    def _check_whitelist(self, item):
        """Returns True if the item is whitelisted, False otherwise.
        """
        if str(item.subreddit).lower() in self._whitelist or item.id in self._whitelist_ids:
            return True
        if self._whitelist_distinguished and item.distinguished:
            return True
        if self._whitelist_gilded and item.gilded:
            return True
        if self._max_score is not None and item.score > self._max_score:
            return True
        return False

    def _save_item(self, item):
        with open(os.path.join(self._save_directory, item.id), "w") as fh:
            json.dump(item.json_dict, fh)

    def _remove_submission(self, sub):
        self._logger.info("Deleting submission: #{id} {url}".format(id=sub.id, url=sub.url.encode("utf-8")))

    def _remove_comment(self, comment):
        if self._replacement_format == "random":
            replacement_text = get_sentence()
        elif self._replacement_format == "dot":
            replacement_text = "."
        else:
            replacement_text = self._replacement_format

        short_text = sub(b"\n\r\t", " ", comment.body[:35].encode("utf-8"))
        msg = "/r/{}/ #{} ({}) with: {}".format(comment.subreddit, comment.id, short_text, replacement_text)

        if self._edit_only:
            self._logger.debug("Editing (not removing) {msg}".format(msg=msg))
        else:
            self._logger.debug("Editing and deleting {msg}".format(msg=msg))
        if not self._trial_run:
            comment.edit(replacement_text)
            self._api_calls.append(int(time.time()))

    def _remove(self, item):
        if self._keep_a_copy and self._save_directory:
            self._save_item(item)
        if self._clear_vote:
            try:
                item.clear_vote()
                self._api_calls.append(int(time.time()))
            except HTTPException:
                self._logger.debug("Couldn't clear vote on {item}".format(item=item))
        if isinstance(item, Submission):
            self._remove_submission(item)
        elif isinstance(item, Comment):
            self._remove_comment(item)
        if not self._edit_only and not self._trial_run:
            item.delete()
            self._api_calls.append(int(time.time()))

    def _remove_things(self, items):
        self._logger.info("Loading items to delete...")
        to_delete = [item for item in items]
        self._logger.info("Done. Starting on batch of {} items...".format(len(to_delete)))
        for idx, item in enumerate(to_delete):
            minute_ago = arrow.now().replace(minutes=-1).timestamp
            self._api_calls = [api_call for api_call in self._api_calls if api_call >= minute_ago]
            if len(self._api_calls) >= 60:
                self._logger.info("Sleeping 10 seconds to wait out API cooldown...")
                time.sleep(10)
            self._logger.debug("Examining item {}: {}".format(idx + 1, item))
            created = arrow.get(item.created_utc)
            if str(item.subreddit).lower() in self._blacklist:
                self._logger.debug("Deleting due to blacklist")
                self._remove(item)
            elif self._check_whitelist(item):
                self._logger.debug("Skipping due to: whitelisted")
                continue
            if created <= self._nuke_cutoff:
                self._logger.debug("Item occurs prior to nuke cutoff")
                self._remove(item)
            elif created > self._recent_cutoff:
                self._logger.debug("Skipping due to: too recent")
                continue
            else:
                self._remove(item)
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
