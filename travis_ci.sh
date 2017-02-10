#!/usr/bin/env bash
coverage3 run travis_ci.py
coverage3 report
cp platformio.ini travis_ci
cd travis_ci
pio run
