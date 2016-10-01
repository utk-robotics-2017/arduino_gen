import sys
import os
import argparse
import re
import subprocess

# argument inputs
parse = argparse.ArgumentParser(description = "Manages Arduinos")
parse.add_argument("-d", action="store", dest="devNum")
parse.add_argument("-n", action="store", dest="devNameListed")
parse.add_argument("-l", action="store_true", default=False, dest="listDevs")
parse.add_argument("-r", action="store_true", default=False, dest="devRemove")

args = parse.parse_args()

# argument deal-with-er
devNum = args.devNum
devNameListed = args.devNameListed
listDevs = args.listDevs
devRemove = args.devRemove

#argument checker
# check if root
if listDevs and (devNameListed or (devNum != None)):
    print("You cannot list devices and add an arduino at the same time.")
    sys.exit()
elif listDevs:
    arduinoNames = os.listdir("/etc/udev/rules.d")
    for i in arduinoNames:
        print(i)

# dev lisit

