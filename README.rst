Shreddit
###########

Details
-----------
Uses the praw over at https://github.com/praw-dev/praw to do all the heavy lifting.

Usage
-----------
- Just run `./schreddit`
- You will need the `praw` Reddit Python library installed somewhere. I advise taking a read of https://github.com/praw-dev/praw#installation

Tit-bits
-----------
- If you fill in your user/passwd in your reddit.cfg then you won't be asked for login details when you run the program! Otherwise you'll be prompted every time.

Cron examples
-----------
- Run crontab -e to edit your cron file. If you have access to something like vixie-cron then each user can have their own personal cron job!

- Run every hour on the hour
	`0 * * * * cd /home/$USER/Shreddit/; ./shreddit`

- Run at 3am every morning
	`0 3 * * * cd /home/$USER/Shreddit/; ./shreddit`

- Run once a month on the 1st of the month
	`0 0 1 * * cd /home/$USER/Shreddit/; ./shreddit`

Caveats
-----------
- Only your previous 1,000 comments are accessable on Reddit. So good luck deleting the others. There may be ways to hack around this via iterating using sorting by top/best/controversial/new but for now I am unsure. I believe it best to set the script settings and run it as a cron job and then it won't be a problem unless you post *a lot*

- Would make life easier if Reddit just did a "DELETE * FROM abc_def WHERE user_id = 1337"

- You require the reddit python library somewhere in your PYTHONPATH

Donations
----------
If you enjoy the added privacy from this script consider donating a tiny wee bit to myself, I will love you forever if you do!
17x7Zp3SKGMJu7S3MGa5ktKVDj4ZVAqB14
