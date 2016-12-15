#!/usr/bin/env bash
cd /Robot/CurrentArduinoCode/stage4
git add -A
git commit -m "new uploaded arduino code for stage4"
git push
pio run -t upload
