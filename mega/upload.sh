#!/usr/bin/env bash
sh build.sh
git add -A
git commit -m "new uploaded arduino code for mega"
git push
ino upload -m mega2560 -p /dev/mega
