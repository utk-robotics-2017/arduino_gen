import argparse
import json
from sensors.ultrasonics import ultrasonics
from sensors.linesensors import linesensors
from sensors.i2cencoders import i2cencoders
from sensors.encoders import encoders
from sensors.switches import switches
from actuators.servos import servos
from special.arms import arms
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
        sensor_dict['ultrasonic'].add(json_item['label'], json_item['pin'])
    elif json_item['type'] == 'linesensor':
        if not 'linesensor' in sensor_dict:
            sensor_dict['linesensor'] = linesensors()
        sensor_dict['linesensor'].add(json_item['label'], json_item['pin'])
    elif json_item['type'] == 'i2cencoder':
        if not 'i2cencoder' in sensor_dict:
            sensor_dict['i2cencoder'] = i2cencoders()
        sensor_dict['i2cencoder'].add(json_item['label'], json_item['pinA'], json_item['pinB'], json_item['reverse'], json_item['init_number'])
    elif json_item['type'] == 'encoder':
        if not 'encoder' in sensor_dict:
            sensor_dict['encoders'] = encoders()
        sensor_dict['encoders'].add(json_item['label'], json_item['pinA'], json_item['pinB'])
    elif json_item['type'] in ['switch', 'button', 'limit_switch']:
        if not 'switch' in sensor_dict:
            sensor_dict['switch'] = switches()
        sensor_dict['switch'].add(json_item['label'], json_item['pin'], json_item['pullup'])
    elif json_item['type'] == 'servo':
        if not 'servo' in sensor_dict:
            sensor_dict['servo'] = servos()
        sensor_dict['servo'].add(json_item['label'], json_item['pin'])
    elif json_item['type'] == 'arm':
        if not 'arm ' in sensor_dict:
            sensor_dict['arm'] = arms()
        sensor_dict['arm'].add(json_item['label'], json_item['base_pin'], json_item['shoulder_pin'], json_item['elbow_pin'], json_item['wrist_pin'], json_item['wrist_rotate_pin'])

gen = generator(sensor_dict)

fo.write(gen.add_header())
fo.write(gen.add_includes())
fo.write(gen.add_pins())
fo.write(gen.add_constructors())
fo.write(gen.add_setup())
fo.write(gen.add_template(1))
fo.write(gen.add_commands())
fo.write(gen.add_template(2))
fo.write("\n")
