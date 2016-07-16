"""Setup script for shreddit.
"""
from setuptools import setup
from codecs import open
from os import path

VERSION = "2.0.0"
DESCRIPTION = " Remove your comment history on Reddit as deleting an account does not do so."

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding='utf-8') as filein:
    long_description = filein.read()

with open(path.join(here, "requirements.txt"), encoding="utf-8") as filein:
    requirements = [line.strip() for line in filein.readlines()]

setup(
    name="shreddit",
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    url="https://github.com/scott-hand/Shreddit",
    author="Scott Hand",
    author_email="scott@vkgfx.com",
    classifiers=["Development Status :: 3 - Alpha",
                 "Intended Audience :: End Users/Desktop",
                 "Programming Language :: Python :: 2"],
    packages=["shreddit"],
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "shreddit=shreddit.app:main"
        ]
    }
)
