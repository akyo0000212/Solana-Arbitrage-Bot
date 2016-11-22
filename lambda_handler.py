"""This module contains the handler function called by AWS.
"""
from shreddit.shredder import shred
import yaml


def lambda_handler(event, context):
    with open("shreddit.yml") as fh:
        config = yaml.safe_load(fh)
    if not config:
        raise Exception("No config options passed!")
    shred(config)
