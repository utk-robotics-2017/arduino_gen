#!/usr/bin/env bash
coverage3 run travis_ci.py
cp platformio.ini travis_ci
cd travis_ci
coverage3 report
pio run
