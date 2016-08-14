#!/usr/bin/env bash
rm -r /currentArduinoCode/mega
cp -r /home/andrew/ArduinoGen/mega /currentArduinoCode/mega
cd /currentArduinoCode/mega
sh build.sh
rm upload_copy.sh
git add -A
git commit -m "new uploaded arduino code for mega"
git push
ino upload -m mega2560 -p /dev/mega
chmod -r 0777 .