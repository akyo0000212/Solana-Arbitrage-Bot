"""This module contains script entrypoints for shreddit.
"""
import argparse
import yaml
import logging
import os
import pkg_resources
from shreddit import default_config
from shreddit.shredder import Shredder


def main():
    parser = argparse.ArgumentParser(description="Command-line frontend to the shreddit library.")
    parser.add_argument("-c", "--config", help="Config file to use instead of the default shreddit.yml")
    parser.add_argument("-u", "--user", help="User section from praw.ini if not default", default="default")
    args = parser.parse_args()

    config_filename = args.config or "shreddit.yml"
    if not os.path.isfile(config_filename):
        print("No configuration file could be found. Paste the following into a file called \"shreddit.yml\" and " \
                "try running shreddit again:\n\n")
        print(pkg_resources.resource_string("shreddit", "shreddit.yml.example"))
        return

    with open(config_filename) as fh:
        # Not doing a simple update() here because it's preferable to only set attributes that are "whitelisted" as
        # configuration options in the form of default values.
        user_config = yaml.safe_load(fh)
        for option in default_config:
            if option in user_config:
                default_config[option] = user_config[option]

    shredder = Shredder(default_config, args.user)
    shredder.shred()


if __name__ == "__main__":
    main()
