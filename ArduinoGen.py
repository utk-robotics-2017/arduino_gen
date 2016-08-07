#includes
import argparse
import json
import os
import shutil
import getpass

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
from actuators.steppers import steppers

# Control Includes
from control.pids import pids

#Systems Includes
from systems.arms import arms
from systems.velocitycontrolledmotors import velocitycontrolledmotors
from systems.fourwheeldrivebases import fourwheeldrivebases

from generator import Generator

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
CURRENT_ARDUINO_CODE_DIR = "/home/pi/../../../currentArduinoCode"


class ArduinoGen:
    def __init__(self, **kwargs):
        self.arduino = kwargs.get("arduino", "")


        print "Making directory...",

        self.arduino_folder = "%s/%s" % (CURRENT_DIR, self.arduino)
        if os.path.exists(self.arduino_folder):
            shutil.rmtree(self.arduino_folder)
        os.makedirs(self.arduino_folder, 0777)
        os.makedirs("%s/src" % self.arduino_folder, 0777)
        print "Done"

        jsonFile = "%s/conf/%s.json" % (CURRENT_DIR, self.arduino)

        print "Copying config file...",

        shutil.copyfile(jsonFile, "%s/%s.json" % (self.arduino_folder, self.arduino))
        print "Done"

        print "Reading config file...",
        self.device_dict = dict()
        self.read_input(open(jsonFile))
        
        print "Done"

        print "Generating output..."
        upload = kwargs.get('upload', False)
        self.generate_output(open("%s/src/%s.ino" % (self.arduino_folder, self.arduino), 'w'), upload)
        print "Done"
        if upload:
            self.upload()
        else:
            build = kwargs.get('build', False)
            if build:
                self.build()
        print "Finished."

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
                else:
                    self.device_dict[json_item['type']].add(json_item)

    def generate_output(self, fo, upload):
        gen = Generator(self.device_dict)
        print "\tWriting headers"
        fo.write(gen.add_header())
        print "\tWriting includes"
        fo.write(gen.add_includes())
        print "\tWriting pins"
        fo.write(gen.add_pins())
        print "\tWriting constructors"
        fo.write(gen.add_constructors())
        print "\tWriting setup"
        fo.write(gen.add_setup())
        print "\tWriting loop"
        fo.write(gen.add_loop())
        print "\tWriting parse args"
        fo.write(gen.add_parse_args())
        print "\tWriting check input"
        fo.write(gen.add_check_input())
        print "\tWriting parse and execute command"
        fo.write(gen.add_parse_and_execute_command_beginning())
        fo.write(gen.add_commands())
        fo.write(gen.add_parse_and_execute_command_ending())
        print "\tWriting extra functions"
        fo.write(gen.add_extra_functions())
        fo.write("\n")
        print "\tCopying include files"
        gen.copy_include_files(self.arduino_folder)
        print "\tWriting build, serial, and upload shell scripts"
        gen.write_shell_scripts(self.arduino_folder, self.arduino, upload)

    def build(self):
        os.chdir("%s/%s" % (CURRENT_DIR, self.arduino))
        os.system("sudo sh build.sh")

    def upload(self):
        os.chdir("%s/%s" % (CURRENT_DIR, self.arduino))
        os.system("sudo sh upload_copy.sh")


if __name__ == "main":
    # Collect command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="Path to the config file for what is connected to the arduino")
    ap.add_argument("-b", "--build", required=False, help="Build the ino file into something that can be uploaded to the arduino")
    ap.add_argument("-u", "--upload", required=False, help="Build the ino file and upload that on to the arduino")
    args = vars(ap.parse_args())

    ArduinoGen(input=args['input'], build=args['build'], upload=args['upload'], prefix="../")
