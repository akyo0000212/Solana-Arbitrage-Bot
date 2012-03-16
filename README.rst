Shreddit
###########

Details
-----------
When one deletes their account on Reddit it does nothing with their comment history other than
obscure the author (replaces with [deleted]) which is not good enough for some people.

Usage
-----------
python2 shreddit.py UserName

Caveats
-----------
- Only your previous 1,000 comments are accessable on Reddit. So good luck deleting the others. There may be ways to hack around this via iterating using sorting by top/best/controversial/new but for now I am unsure.

- Would make life easier if Reddit just did a "DELETE * FROM abc_def WHERE user_id = 1337"
