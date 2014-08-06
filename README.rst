Shreddit
###########

Details
-----------
Shreddit is a Python command line program which will take a user's post history on the website Reddit (http://reddit.com) and after having the user edit a config file will systematically go through the user's history deleting one post/submission at a time utnil only those whitelisted remain.
Note: When it became known that post edits were *not* saved but post deletions *were* saved code was added to edit your post prior to deletion. In fact you can actually turn off deletion all together and just have lorem ipsum (or a message about Shreddit) but this will increase how long it takes the script to run as it will be going over all of your messages every run!
Basically it lets you maintain your normal reddit account while having your history scrubbed after a certain amount of time.
Uses PRAW over at https://github.com/praw-dev/praw to do all the heavy lifting.

Usage & Installation
-----------
I highly advise setting up a virtual environment for Python locally (via the `virtualenv` command) and from there you'll be able to run `source bin/activate` and then `pip install -r requirements.txt`
and that will install everything that's required to run the script.

After that you'll simply want to run `python shreddit.py -c config_file.cfg` or set up a cron job to do it periodically.

Alternatively you may install the requirements (see requirements.txt) from your distro if they are there.

Tit-bits
-----------
- If you fill in your user/passwd in your reddit.cfg then you won't be asked for login details when you run the program! Otherwise you'll be prompted every time.

Cron examples
-----------
- Run crontab -e to edit your cron file. If you have access to something like vixie-cron then each user can have their own personal cron job!

- Run every hour on the hour
	`0 * * * * cd /home/$USER/Shreddit/ && source bin/activate && ./shreddit.py`

- Run at 3am every morning
	`0 3 * * * cd /home/$USER/Shreddit/ && source bin/activate && ./shreddit.py`

- Run once a month on the 1st of the month
	`0 0 1 * * cd /home/$USER/Shreddit/ && source bin/activate && ./shreddit.py`

Caveats
-----------
- Only your previous 1,000 comments are accessable on Reddit. So good luck deleting the others. There may be ways to hack around this via iterating using sorting by top/best/controversial/new but for now I am unsure. I believe it best to set the script settings and run it as a cron job and then it won't be a problem unless you post *a lot*. I do, however, think that it may be a caching issue and perhaps after a certain time period your post history would, once again, become available as a block of 1,000. So you needn't despair yet!

- Would make life easier if Reddit just did a "DELETE * FROM abc_def WHERE user_id = 1337"

- We are relying on Reddit admin words that they do not store edits.
