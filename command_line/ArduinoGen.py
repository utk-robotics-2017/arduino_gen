import argparse
import json
from sensors.ultrasonics import ultrasonics
from sensors.linesensors import linesensors
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

sensor_dict = dict()

for json_item in json_data:
    if json_item['type'] == 'ultrasonic':
        if not 'ultrasonic' in sensor_dict:
            sensor_dict['ultrasonic'] = ultrasonics()
        sensor_dict['ultrasonic'].add_sensor(json_item['label'], json_item['pin'])
    elif json_item['type'] == 'linesensor':
        if not 'linesensor' in sensor_dict:
            sensor_dict['linesensor'] = linesensors()
        sensor_dict['linesensor'].add_sensor(json_item['label'], json_item['pin'])

gen = generator(sensor_dict)

fo.write(gen.add_header())
fo.write(gen.add_includes())
fo.write(gen.add_pins())
fo.write(gen.add_constructors())
fo.write(gen.add_setup())
fo.write(gen.add_template(1))
fo.write(gen.add_sensor_commands())
fo.write(gen.add_template(2))
fo.write("\n")
