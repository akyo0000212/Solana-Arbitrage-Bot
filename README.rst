Shreddit
###########

Details
-----------
Uses the reddit_api over at https://github.com/mellort/reddit_api to do all the heavy lifting.

Usage
-----------
- Just run `./schreddit`
- You may want to check out the reddit_api, build it using `python setup.py build` and then copy the /reddit directory to this directory. The reason I don't provide it is that the reddit_api changes frequently and I don't want to include a static old version here. I also don't want to have a git repo in a git repo.

Tit-bits
-----------
- If you fill in your user/passwd in your reddit_api then you won't be asked for login details when you run the program! Otherwise you'll be prompted every time.

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
