Shreddit
###########

Details
-----------
Uses the reddit_api over at https://github.com/mellort/reddit_api to do all the heavy lifting.

Usage
-----------
- Just run `./schreddit`

Caveats
-----------
- Only your previous 1,000 comments are accessable on Reddit. So good luck deleting the others. There may be ways to hack around this via iterating using sorting by top/best/controversial/new but for now I am unsure. I believe it best to set the script settings and run it as a cron job and then it won't be a problem unless you post *a lot*

- Would make life easier if Reddit just did a "DELETE * FROM abc_def WHERE user_id = 1337"
