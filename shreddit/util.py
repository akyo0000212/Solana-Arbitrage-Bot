"""This module contains common utilities for the rest of the package.
"""
import random


WORDLIST = "/usr/share/dict/words"
STATIC_TEXT = "I have been Shreddited for privacy!"


try:
    from loremipsum import get_sentence
except ImportError:
    def get_sentence():
        """This keeps the mess of dealing with the loremipsum library out of the shredding code. Until the maintainer of
        the loremipsum package uploads a version that works with Python 3 to pypi, it is necessary to provide a drop-in
        replacement. The current solution is to return a static text string unless the operating system has a word list.
        If that is the case, use it instead.
        """
        try:
            lines = [line.strip() for line in open(WORDLIST).readlines()]
            return " ".join(random.sample(lines, random.randint(50, 150)))
        except IOError:
            # The word list wasn't available...
            return STATIC_TEXT
