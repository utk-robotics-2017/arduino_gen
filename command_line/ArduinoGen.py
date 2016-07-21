#includes
import argparse
import json
import os
import shutil

# Sensor Includes
from sensors.ultrasonics import ultrasonics
from sensors.linesensors import linesensors
from sensors.i2cencoders import i2cencoders
from sensors.encoders import encoders
from sensors.switches import switches
from sensors.linesensor_arrays import linesensor_arrays

# Actuator Includes
from actuators.servos import servos
from actuators.motors import motors

# Control Includes
from control.pids import pids

#Systems Includes
from systems.arms import arms
from systems.velocitycontrolledmotors import velocitycontrolledmotors
from systems.fourwheeldrivebases import fourwheeldrivebases

from generator import generator

class ArduinoGen:
    def __init__(self, **kwargs):
        _input = kwargs.get("input", "")

        dot = _input.rfind(".")
        lastSlash = args["input"].rfind("/")
        self.arduino = args["input"][:dot][lastSlash:]
        self.arduino_folder = "../../" + self.arduino
        if os.path.exists(self.arduino_folder):
            shutil.rmtree(self.arduino_folder)
        os.makedirs(self.arduino_folder)

        shutil.copyfile(_input, self.arduino_folder + "/" + arduino + ".json")

        self.device_dict = dict()
        self.read_input(open(_input))
        self.generate_output(open(self.arduino_folder+ "/%s.ino" % (arduino), 'w'))

        upload = kwargs.get('upload', False)
        if upload:
            build()
            upload()
        else:
            build = kwargs.get('build', False)
            if build:
                build()

    def read_input(self, fi):
        # Read in json
        file_text = ""
        for line in fi:
            file_text = file_text + line
        json_data = json.loads(file_text)

        #Split into levels based on dependencies
        device_type = [
            {
                'ultrasonic': ultrasonics(),
                'linesensor': linesensors(),
                'i2cencoder': i2cencoders(),
                'encoder': encoders(),
                'switch': switches(),
                'servo': servos(),
                'motor': motors(),
                'pid': pids(),
                'linesensor_array': linesensor_arrays(),
                'stepper': steppers()
            },
            {
                'arm': arms(),
                'velocityControlledMotor': velocitycontrolledmotors()
            },
            {
                'fourWheelDriveBase': fourwheeldrivebases()
            }
            ]

            for device_level in device_type:
                for json_item in json_data:

                    # Buttons and Limit Switches work the same as switches
                    if json_item['type'].lower() == 'limit_switch' or json_item['type'].lower() == 'button':
                        json_item['type'] = 'switch'
                    # Setup the motor controller
                    if json_item['type'].lower() == 'monstermotomotor':
                        json_item['type'] = 'motor'
                        json_item['motorController'] = 'monsterMoto'
                    elif json_item['type'].lower() == 'roverfivemotor':
                        json_item['type'] = 'motor'
                        json_item['motorController'] = 'roverFive'

                    if not json_item['type'] in device_level:
                        continue

                    if not json_item['type'] in self.device_dict:
                        self.device_dict[json_item['type']] = device_level[json_item['type']]

                    if json_item['type'] == 'arm':
                        self.device_dict[json_item['type']].add(json_item, self.device_dict['servo'])
                    elif json_item['type'] == 'velocityControlledMotors':
                        self.device_dict[json_item['type']].add(json_item, self.device_dict['motor'], self.device_dict['i2cencoder'], self.device_dict['vpid'])
                    elif json_item['type'] == 'fourWheelDriveBase':
                        self.device_dict[json_item['type']].add(json_item, self.device_dict['motor'], self.device_dict['velocitycontrolledmotor'])

                    self.device_dict[json_item['type']].add(json_item)
    def generate_output(self, fo):
        gen = generator(self.device_dict)
        fo.write(gen.add_header())
        fo.write(gen.add_includes())
        fo.write(gen.add_pins())
        fo.write(gen.add_constructors())
        fo.write(gen.add_setup())
        fo.write(gen.add_loop())
        fo.write(gen.add_parse_args())
        fo.write(gen.add_check_input())
        fo.write(gen.add_parse_and_execute_command_beginning())
        fo.write(gen.add_commands())
        fo.write(gen.add_parse_and_execute_command_ending())
        fo.write(gen.add_extra_functions())
        fo.write("\n")
        gen.copy_include_files(self.arduino_folder)
        gen.copy_shell_scripts(self.arduino_folder)

    def build(self):
        exec(self.arduino_folder + "/build.sh")

    def upload(self):
        exec(self.arduino_folder + "/upload.sh")


if __init__ == "main":
    # Collect command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="Path to the config file for what is connected to the arduino")
    ap.add_argument("-b", "--build", required=False, help="Build the ino file into something that can be uploaded to the arduino")
    ap.add_argument("-u", "--upload", required=False, help="Build the ino file and upload that on to the arduino")
    args = vars(ap.parse_args())

    ArduinoGen(input=args['input'], build=args['build'], upload=args['upload'])
