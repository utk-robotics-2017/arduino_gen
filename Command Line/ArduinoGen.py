import argparse
import json
from Sensors.ultrasonic import ultrasonic
from generator import generator
import os

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="Path to the config file for what is connected to the arduino")
args = vars(ap.parse_args())

fi = open(args["input"], "r")
dot = args["input"].find(".")
fo_prefix = args["input"][:dot]
if not os.path.exists(fo_prefix):
    os.makedirs(fo_prefix)
fo = open("%s/%s.ino" % (fo_prefix, fo_prefix), "w")

file_text = ""
for line in fi:
    file_text = file_text + line

json_data = json.loads(file_text)

sensor_list = []

for json_item in json_data:
    if json_item['type'] == 'ultrasonic':
        sensor_list.append(ultrasonic(json_item['id'], json_item['pin']))

gen = generator(sensor_list)

fo.write(gen.add_includes())
fo.write("\n");
fo.write(gen.add_pins())
fo.write("\n");
fo.write(gen.add_constructors())
