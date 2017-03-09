#!/usr/bin/env bash
coverage3 run travis_ci.py
coverage3 report
echo "=== Generated Code: ==="
cat travis_ci/src/travis_ci.ino
cp platformio.ini travis_ci
echo "=== Compiling: ==="
cd travis_ci
pio run
