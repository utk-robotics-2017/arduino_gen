#!/usr/bin/env bash
python3 travis_ci.py
cp platformio.ini travis_ci
pio run
