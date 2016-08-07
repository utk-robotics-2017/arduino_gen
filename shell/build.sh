#!/usr/bin/env bash

hashes=$(sha1sum `find src/ -type f` | tr '\n' ',' | tr ' ' '-')
ino build -m mega2560 --cppflags="-D __USER__=`whoami` -D __DIR__=`pwd` -D __GIT_HASH__=`git rev-parse HEAD`"
