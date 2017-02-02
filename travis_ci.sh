#!/usr/bin/env bash
coverage run travis_ci.py
cp platformio.ini travis_ci
cd travis_ci
pio run

coverage report
