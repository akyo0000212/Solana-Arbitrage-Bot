#!/usr/bin/env sh

virtualenv .
source ./bin/activate
pip install -r requirements.txt

if [ ! -f "shreddit.cfg" ]; then
	cp "shreddit.cfg.example" "shreddit.cfg"
	$EDITOR shreddit.cfg
fi

