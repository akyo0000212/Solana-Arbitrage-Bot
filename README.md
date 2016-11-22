Shreddit
========

YAML Upgrade
------------

**Note! Important! The latest version uses YAML format over the old
simpleconfigparser! This means you'll have to migrate your config file to
yaml!**

User Login deprecation
----------------------

Reddit intends to disable username-password based authentication to access its
APIs in the near future. You can specify your username and password in the
`shreddit.yml` or the `praw.ini` to make it work **FOR NOW**. But consider
looking at the [OAuth2 instructions](#oauth2-instructions) if you intend to use
this program in the future.

Description
-----------

Shreddit is a Python command line program which will take a user's post history
on the website [Reddit](http://reddit.com), and will systematically go through
the user's history deleting one post/submission at a time until only those
whitelisted remain.

**Note:** When it became known that post edits were *not* saved but post
deletions *were* saved, code was added to edit your post prior to deletion. In
fact you can actually turn off deletion all together and just have lorem ipsum
(or a message about Shreddit) but this will increase how long it takes the
script to run as it will be going over all of your messages every run!

It allows you to maintain your normal reddit account while having your history
scrubbed after a certain amount of time.

Installation ([Click here for Windows instructions](#for-windows-users))
------------------------------------------------------------------------
The way I personally install Shreddit is via a handy tool called `virtualenv`
which may come with your package manager or may be a part of your Python package
in your distro (have a search if you can't find it). Both Python 2 and 3 are
supported.

1. Clone the repository
2. Enter the repository's directory and run `virtualenv .` (this creates a 
   virtual environment)
3. Run the following command, you must run this *every time* you wish to run
   the script `source ./bin/activate`.
4. This installs the required modules locally to your Shreddit virtual
   environment `pip install -r requirements.txt`.
5. Copy `shreddit.yml.example` to something else and edit it to your liking.
	- Make sure you specify your username and password in the file.
	- See the [OAuth2 instructions](#oauth2-instructions) if you don't want to
      use username-password based authentication.

Notes:

- The script *does* work with Python versions 2 and 3 but people often get in a
  mess with pip versions, python versions and virtulenv versions. Make sure
  that your Python/pip/virtualenv are all the same version. If you ran the above
  code it *should* work as stated.
- If in doubt try running `python3` instead of just `python` - the same goes for
  `pip3` and `virtualenv3` (exchange for 2 if you wish, though I advise using
  version 2).
- It's useful to have it run as an event, you can set this up as you like but I
  suggest `cron` via `crontab -e` and adding a line such as 
  `@hourly cd $HOME/Shreddit && source bin/activate && shreddit` See below for
  more.
- Adding your password to the praw.ini and adding the additional output line
  can provide extra debugging help.

Cron examples
-------------

- Run `crontab -e` to edit your cron file. If you have access to something like
  vixie-cron then each user can have their own personal cron job!

- Run every hour on the hour
	`0 * * * * cd /home/$USER/Shreddit/ && source bin/activate && ./shreddit.py`

- Run at 3am every morning
	`0 3 * * * cd /home/$USER/Shreddit/ && source bin/activate && ./shreddit.py`

- Run once a month on the 1st of the month
	`0 0 1 * * cd /home/$USER/Shreddit/ && source bin/activate && ./shreddit.py`

If for some reason you get an error saying `source: not found` in your logs,
change `source` to `.`. The source command would become `. bin/activate`. This
is caused by your cron jobs running in shell, not bash, and the source command
is a dot.

For Windows users
-----------------

1. Make sure you have Python installed. 
   [Click here for the Python download page](https://www.python.org/downloads/).
	- **Note:** Install either `python 2.x` or `python 3.x`, not both.
2. Clone the repository (or download and extract the
   [zip file](https://github.com/dragsubil/Shreddit/archive/master.zip))
3. Open command prompt and type `cd <path to the Shreddit folder>`
4. Type `pip install -r requirements.txt` in the open command prompt window to
   download and install the required additional modules.
5. Open the `shreddit.yml.example` and edit it to your liking and rename the
   file to `shreddit.yml`.
	- Make sure you specify your username and password in the file.
	- See the [OAuth2 instructions](#oauth2-instructions) if you don't want to
      use username-password based authentication.
6. Type `shreddit` in the open command prompt window to run the program.

OAuth2 Instructions
-------------------

1. Visit: https://www.reddit.com/prefs/apps
2. Click on 'Create app'. 
	- Fill in the name and select the 'script' option
	- Under "redirect uri" put http://127.0.0.1:65010
3. Copy from or rename `praw.ini.example` to `praw.ini` and open it. Enter the
   values from the Reddit page.
	- oauth\_client\_id = { The ID displayed next to the icon thingy (under
      "personal use script") }
	- oauth\_client\_secret = { The secret }
	- oauth\_redirect\_uri = http://127.0.0.1:65010
	- Save the file.
4. Run `python get_secret.py` in the command prompt.
5. Your browser will open to a page on Reddit listing requested permissions.
6. Click 'Allow'.


Caveats
-------

- Certain limitations in the Reddit API and the PRAW library make it difficult
  to delete more than 1,000 comments. While deleting >1000 comments is planned,
  it is necessary right now to rerun the program until they are all deleted.

- We are relying on Reddit admin words that they do not store edits, deleted
  posts are still stored in the database they are merely inaccessible to the
  public.
