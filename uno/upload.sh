#!/usr/bin/env bash
sh build.sh
git add -A
git commit -m "new uploaded arduino code for uno"
git push
ino upload -m uno -p /dev/uno
