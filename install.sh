#!/usr/bin/env sh

virtualenv .
source ./bin/activate
pip install -r requirements.txt

if [ ! -f "shreddit.yml" ]; then
	cp "shreddit.yml.example" "shreddit.yml"
	$EDITOR shreddit.yml
fi

