#!/usr/bin/env bash
find /currentArduinoCode/uno/* -not -name 'ProductName' -delete
cp -r /home/andrew/ArduinoGen/uno /currentArduinoCode
cd /currentArduinoCode/uno
sh build.sh
rm upload_copy.sh
git add -A
git commit -m "new uploaded arduino code for uno"
git push
ino upload -m uno -p /dev/uno
chmod -R +0777 .