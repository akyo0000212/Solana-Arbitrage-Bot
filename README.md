# Shreddit

Shreddit is a Python command line program which will take a user's post history on the website
[Reddit](http://reddit.com), and will systematically go through the user's history deleting one post/submission at a
time until only those whitelisted remain. It allows you to maintain your normal reddit account while having your history
scrubbed after a certain amount of time.

When it became known that post edits were *not* saved but post deletions *were* saved, code was added to edit your post
prior to deletion. In fact you can actually turn off deletion all together and just have lorem ipsum (or a message
about Shreddit) but this will increase how long it takes the script to run as it will be going over all of your messages
every run.

I added some changes. Namely, the command will run to completion (ie, it's fire and forget now). I also took the liberty
of making the "batch_limit" configurable in the "shreddit.yaml" file. However, that option is pretty much unnecessary because
I fixed the API limit error from breaking shreddit. Instead, the exception will be handled gracefully, and the process will
continue until all comments and posts have been considered for deletion. 

## Pip Installation

I personally recommend using the manual instructions. This is a forked brank of shreddit containing fixes not in the 
main branch. Your mileage will vary if you use pip to install it.

`pip install -U shreddit` will install the package and its dependencies, and it will add a `shreddit` command line
utility to your PATH. This is typically either run in a virtualenv or using administrative privileges for global
installation.

## Manual Installation

1. Clone the `shreddit` repository to a directory.
2. From the directory, run `pip install -r requirements.txt`
3. Run `python setup.py install` to install the package and the `shreddit` command line utility.  This is typically
   either run in a virtualenv or using administrative privileges for global installation.

Note: The original author limited some of the requirement versions for packages. I found most of those errors are
resolved running "pip install <package-name> --upgrade".

## Usage

After installing the `shreddit` command line utility, the first step is setting up the tool's configuration files.
Simply typing `shreddit -g` will generate configs. After configuring credentials, running the tool with the `shreddit`
command will begin the tool's operation.

### Configuring Credentials

Running `shreddit -g` will generate a blank praw.ini file that looks like this:

```
# Credentials go here. Fill out default, or provide one or more names and call shreddit with the -u option to specify
# which set to use.
[default]
client_id=
client_secret=
username=
password=
```

**You must provide values for each of these.** As strange as it may seem to provide both a username/password pair *and*
a client id/secret pair, that is how the Reddit API does "OAuth" script applications.

Username and password are simply your Reddit login credentials for the account that will be used. However, to obtain the
client ID and secret, follow these steps (taken from 
[PRAW documentation](http://praw.readthedocs.io/en/latest/getting_started/authentication.html#script-application)):

1. Open your Reddit application preferences by clicking [here](https://www.reddit.com/prefs/apps/).
2. Add a new application. It doesn't matter what it's named, but calling it "shreddit" makes it easier to remember. The button will probably say something about being a developer, don't worry, its fine.
3. Select "script".
4. Redirect URL does not matter for script applications, so enter something like http://127.0.0.1:8080
5. Once created, you should see the name of your application followed by 14 character string. Enter this 14 character
   string as your `client_id`.
6. Copy the 27 character "secret" string into the `client_secret` field.

Finally, your praw.ini should look like this (with fake data provided here):

```
[default]
client_id=f3FaKeD4t40PsJ
client_secret=dfK3pfMoReFAkEDaTa123456789
username=testuser
password=123passwordgoeshere123
```

Keep your praw.ini either in the current directory when running `shreddit`, or in one of the config folders
[described here](http://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html) such as
`~/.config` in Linux or `%APPDATA%` in Windows.

To use more than one account, you can add multiple profiles instead of just `[default]` and use the `-u` option to 
`shreddit` to choose which one each time.

### Automating

The easiest way to automate this tool after the first run is by using the cron utility. Run `crontab -e` to edit your
user's crontab settings.

**Examples:**

The following examples require that the PRAW configuration file is located in the config directory. See [this PRAW
documentation](http://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html) for more information.

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
usage: app.py [-h] [-c CONFIG] [-g] [-u USER]

Command-line frontend to the shreddit library.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file to use instead of the default shreddit.yml
  -g, --generate-configs
                        Write shreddit and praw config files to current
                        directory.
  -u USER, --user USER  User section from praw.ini if not default
```

## For Windows users

I highly recommend installing WSL and using the manual installation instructions. 

Or (from the original author):

1. Make sure you have Python installed.
   [Click here for the Python download page](https://www.python.org/downloads/).
        - **Note:** Install either `python 2.x` or `python 3.x`, not both.
2. Follow the [pip installation](#pip-installation) instructions.
3. Open a new command prompt and verify that the `shreddit` command works before moving on to the [usage](#usage)
   section.

## Caveats

- We are relying on Reddit admin words that they do not store edits, deleted posts are still stored in the database
  they are merely inaccessible to the public.

- Uses a plaintext configuration by default; it might be nice to add some command line parameters for the authentication.

- If you make changes to "shreddit.py", re-running "python setup.py install" will not fix it. You must directly replace
  the file in the python libraries.

- The original author has not updated their repository in about 7 years (since 2016), and many of the requirement version
  from the packages in "requirements.txt" don't work. Most of these can be fixed by running
     - `pip install <package> --upgrade`

- After July 1st, 2023; I have no idea if this will continue working without paying for API access (I think there is a
  severely hampered "free" access to the API, so it might take longer to run after that date, or it might not at all)
