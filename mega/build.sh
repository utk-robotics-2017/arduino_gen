#!/usr/bin/env bash

ino build -m mega2560 --cppflags="-D __USER__=`whoami` -D __DIR_`pwd` -D __GIT_HASH__=`git rev-parse HEAD`"
