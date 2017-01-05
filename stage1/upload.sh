#!/usr/bin/env bash
cd /Robot/CurrentArduinoCode/stage1
git add -A
git commit -m "new uploaded arduino code for stage1"
git push
pio run -t upload
