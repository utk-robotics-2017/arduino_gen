#!/usr/bin/env bash
rm -r /home/pi/../../../currentArduinoCode/mega
cp -r /home/andrew/ArduinoGen/mega /home/pi/../../../currentArduinoCode/mega
cd /home/pi/../../../currentArduinoCode/mega
sh build.sh
rm upload_copy.sh
git add -A
git commit -m "new uploaded arduino code for mega"
git push
