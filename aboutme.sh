#!/usr/bin/env bash

# Custom ASCII hand to replace the :wave: emoji
title="Hi, My name is Piotr"

if command -v figlet &>/dev/null && command -v boxes &>/dev/null; then
	# Using figlet with a standard font for better rendering
	echo "$title" | figlet -f standard -w 200 | boxes -d parchment
else
	echo "$title"
fi

# Optionally, print a custom ASCII hand if figlet or boxes are unavailable
cat <<"EOF"
    o/
EOF
