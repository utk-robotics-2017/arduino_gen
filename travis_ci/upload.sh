#!/usr/bin/env bash
cd /Robot/CurrentArduinoCode/travis_ci
git add -A
git commit -m "new uploaded arduino code for travis_ci"
git push
pio run -t upload
