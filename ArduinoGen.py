#includes
import argparse
import json
import os
import shutil
import getpass
import sys

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

class ArduinoGen:
    def __init__(self, arduino, arduinoType):
        self.arduino = arduino
        self.arduinoType = arduinoType

    def setParentFolder(self, parentFolder):
        self.folder = "%s/%s" % (parentFolder, self.arduino)

    def setupFolder(self):
        if not hasattr(self, 'folder'):
            print "Folder has not been set"
            sys.exit()
        print "Making directory...",
        if os.path.exists(self.folder):
            shutil.rmtree(self.folder)
        os.makedirs(self.folder, 0777)
        os.chmod(self.folder, 0777)
        os.makedirs("%s/src" % self.folder, 0777)
        os.chmod("%s/src" % self.folder, 0777)
        print "Done"

    def readConfig(self, f, copy=True):
        if copy:
            shutil.copyfile(f, "%s/%s.json" % (self.folder, self.arduino))
            os.chmod("%s/%s.json" % (self.folder, self.arduino), 0777)

        print "Reading config file...",
        fi = open(f)
        file_text = fi.read()
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
        self.device_dict = dict()
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
        fi.close()
        print "Done"

    def generateOutput(self):
        if not hasattr(self, 'folder'):
            print "Parent folder has not been set"
            sys.exit()
        elif not hasattr(self, 'device_dict'):
            print "Config file has not been read"
            sys.exit()

        print "Generating output..."
        fo = open("%s/src/%s.ino", (self.folder, self.arduino))
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
        fo.close()
        os.chmod("%s/src/%s.ino" % (self.folder, self.arduino), 0777)

        print "\tCopying include files"
        gen.copy_include_files(self.folder)
        print "\tWriting build, serial, and upload shell scripts"
        gen.write_shell_scripts(self.folder, self.arduino, self.arduinoType)
        print "Done"
        print "Your output can be found at %s/%s" % (self.folder, self.arduino)


    def build(self):
        if not hasattr(self, 'folder'):
            print "Parent folder has not been set"
            sys.exit()
        print "Building..."
        os.chdir("%s/%s" % (self.folder, self.arduino))
        os.system("sh build.sh")
        print "Done"

    def upload(self):
        if not hasattr(self, 'folder'):
            print "Parent folder has not been set"
            sys.exit()
        print "Uploading..."
        os.chdir("%s/%s" % (self.folder, self.arduino))
        os.system("sh upload_copy.sh")
        print "Done"

if __name__ == "__main__":
    # Collect command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--arduino", required=True, help="Name of the arduino")
    ap.add_argument("-pf", "--parent_folder", required=True, help="Parent folder of the folder to put all the output files")
    ap.add_argument("-c", "--config", required=True, help="Location of the config json file")
    ap.add_argument("-b", "--build", required=False, help="Build the ino file into something that can be uploaded to the arduino")
    ap.add_argument("-u", "--upload", required=False, help="Build the ino file and upload that on to the arduino")
    args = vars(ap.parse_args())

    ag = ArduinoGen()
    ag.setParentFolder(args['parent_folder'])
    ag.readConfig(args['config'])
    ag.generateOutput()

    if args['upload']:
        ag.upload()
    elif args['build']:
        ag.build()
