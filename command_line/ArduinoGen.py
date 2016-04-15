#inlcudes
import argparse
import json
import os

# Sensor Includes
from sensors.ultrasonics import ultrasonics
from sensors.linesensors import linesensors
from sensors.i2cencoders import i2cencoders
from sensors.encoders import encoders
from sensors.switches import switches
from sensors.linesensor_arrays import linesensor_arrays

# Actuator Includes
from actuators.servos import servos
from actuators.monsterMotoMotors import monsterMotoMotors

#Special Includes
from special.arms import arms

from generator import generator

# Collect command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="Path to the config file for what is connected to the arduino")
ap.add_argument("-o", "--output", required=False, help="Path to the output file that is the Arduino code")
args = vars(ap.parse_args())

# Set up the input and out files
fi = open(args["input"], "r")

if 'output' in args:
    fo = open(args["output"], "w")
else:
    dot = args["input"].find(".")
    fo_prefix = args["input"][:dot]
    if not os.path.exists(fo_prefix):
        os.makedirs(fo_prefix)
    fo = open("%s/%s.ino" % (fo_prefix, fo_prefix), "w")

# Read in json
file_text = ""
for line in fi:
    file_text = file_text + line
json_data = json.loads(file_text)

device_dict = dict()

device_type = {'ultrasonic': ultrasonics(),
                'linesensor': linesensors(),
                'i2cencoder': i2cencoders(),
                'encoder': encoders(),
                'switch': switches(),
                'servo': servos(),
                'arm': arms(),
                'monsterMotoMotor': monsterMotoMotors(),
                'linesensor_array': linesensor_arrays()}

for json_item in json_data:

    # Buttons and Limit Switches work the same as switches
    if json_item['type'] == 'limit_switch' or json_item['type'] == 'button':
        json_item['type'] = 'switch'

    if not json_item['type'] in device_dict:
        device_dict[json_item['type']] = device_type[json_item['type']]
    device_dict[json_item['type']].add(json_item)

gen = generator(device_dict)

fo.write(gen.add_header())
fo.write(gen.add_includes())
fo.write(gen.add_pins())
fo.write(gen.add_constructors())
fo.write(gen.add_setup())
fo.write(gen.add_template(1))
fo.write(gen.add_commands())
fo.write(gen.add_template(2))
fo.write("\n")
