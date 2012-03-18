Shreddit
###########

Details
-----------
When one deletes their account on Reddit it does nothing with their comment history other than
obscure the author (replaces with [deleted]) which may not be good enough for some.

Usage
-----------
- Add your Reddit details to user.json, should be self explanatory 
- run `./schreddit`

Caveats
-----------
- Only your previous 1,000 comments are accessable on Reddit. So good luck deleting the others. There may be ways to hack around this via iterating using sorting by top/best/controversial/new but for now I am unsure. I believe it best to set the script settings and run it as a cron job and then it won't be a problem unless you post *a lot*

- Would make life easier if Reddit just did a "DELETE * FROM abc_def WHERE user_id = 1337"
