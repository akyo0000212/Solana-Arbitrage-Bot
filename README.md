# Shreddit

Shreddit is a Python command line program which will take a user's post history on the website
[Reddit](http://reddit.com), and will systematically go through the user's history deleting one post/submission at a
time until only those whitelisted remain. It allows you to maintain your normal reddit account while having your history
scrubbed after a certain amount of time.

When it became known that post edits were *not* saved but post deletions *were* saved, code was added to edit your post
prior to deletion. In fact you can actually turn off deletion all together and just have lorem ipsum (or a message
about Shreddit) but this will increase how long it takes the script to run as it will be going over all of your messages
every run.

## User Login deprecation

Reddit intends to disable username-password based authentication to access its APIs in the near future. You can specify
your username and password in the `shreddit.yml` or the `praw.ini` to make it work **FOR NOW**. But consider looking at
the [OAuth2 instructions](#oauth2-instructions) if you intend to use this program in the future.

## Pip Installation

`pip install -U shreddit` will install the package and its dependencies, and it will add a `shreddit` command line
utility to your PATH. This is typically either run in a virtualenv or using administrative privileges for global
installation.

## Manual Installation

1. Clone the `shreddit` repository to a directory.
2. From the directory, run `pip install -r requirements.txt`
3. Run `python setup.py install` to install the package and the `shreddit` command line utility.  This is typically
   either run in a virtualenv or using administrative privileges for global installation.

## Usage

After installing the `shreddit` command line utility, the first step is setting up the tool's configuration file. Simply
typing `shreddit` will print a message with an example config. Copy the message from `---` onwards and save it as
`shreddit.yml`. Now, the tool may be used by simply typing `shreddit` from this directory. Alternatively, if you named
the configuration file something different such as `config.yml`, you may use it with `shreddit -c config.yml`.

### Automating

The easiest way to automate this tool after the first run is by using the cron utility. Run `crontab -e` to edit your
user's crontab settings.

**Examples:**

- Run every hour on the hour
        `0 * * * * shreddit -c <full path to shreddit.yml>`

- Run at 3am every morning
        `0 3 * * * shreddit -c <full path to shreddit.yml>`

- Run once a month on the 1st of the month
        `0 0 1 * * shreddit -c <full path to shreddit.yml>`

If virtualenv was used, be sure to add `source /full/path/to/venv/bin/activate &&` before the command. For example:

`0 * * * * source /full/path/to/venv/bin/activate && shreddit -c <full path to shreddit.yml>`

### Command Line Options

```
$ shreddit --help
usage: shreddit [-h] [-c CONFIG] [-p PRAW] [-t]

Command-line frontend to the shreddit library.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file to use instead of the default shreddit.yml
  -p PRAW, --praw PRAW  PRAW config (if not ./praw.ini)
  -t, --test-oauth      Perform OAuth test and exit
```

## For Windows users

1. Make sure you have Python installed.
   [Click here for the Python download page](https://www.python.org/downloads/).
        - **Note:** Install either `python 2.x` or `python 3.x`, not both.
2. Follow the [pip installation](#pip-installation) instructions.
3. Open a new command prompt and verify that the `shreddit` command works before moving on to the [usage](#usage)
   section.

## OAuth2 Instructions

1. Visit: https://www.reddit.com/prefs/apps
2. Click on 'Create app'.
        - Fill in the name and select the 'script' option
        - Under "redirect uri" put http://127.0.0.1:65010
3. Copy from or rename `praw.ini.example` to `praw.ini` and open it. Enter the values from the Reddit page.
        - oauth\_client\_id = { The ID displayed next to the icon thingy (under
      "personal use script") }
        - oauth\_client\_secret = { The secret }
        - oauth\_redirect\_uri = http://127.0.0.1:65010
        - Save the file.
4. Run `python get_secret.py` in the command prompt.
5. Your browser will open to a page on Reddit listing requested permissions.
6. Click 'Allow'.


## Caveats

- Certain limitations in the Reddit API and the PRAW library make it difficult to delete more than 1,000 comments.
  While deleting >1000 comments is planned, it is necessary right now to rerun the program until they are all deleted.

- We are relying on Reddit admin words that they do not store edits, deleted posts are still stored in the database
  they are merely inaccessible to the public.
