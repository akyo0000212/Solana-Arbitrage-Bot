#!/usr/bin/env sh
if [[ -f './bin/activate' ]]; then
	source ./bin/activate
elif [[ -f '.venv/bin/activate' ]]; then
	source '.venv/bin/activate'
fi	
pip install --upgrade praw
python ./shreddit.py
