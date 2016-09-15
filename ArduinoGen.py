#includes
import argparse
import json
import os
import shutil
import getpass
import sys
import os
import importlib
import glob

from Generator import Generator

# Import all the files in appendages
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
CURRENT_ARDUINO_CODE_DIR = "/Robot/CurrentArduinoCode/"

class ArduinoGen:
    def __init__(self, arduino):
        self.arduino = arduino

    def setParentFolder(self, parentFolder):
        self.folder = "{}/{}".format(parentFolder, self.arduino)

    def setupFolder(self):
        if not hasattr(self, 'folder'):
            print("Folder has not been set")
            sys.exit()
        print("Making directory...")
        if os.path.exists(self.folder):
            shutil.rmtree(self.folder)
        os.makedirs(self.folder, 0o777)
        os.chmod(self.folder, 0o777)
        os.makedirs("{}/src".format(self.folder), 0o777)
        os.chmod("{}/src".format(self.folder), 0o777)
        print("Done")

    def readConfig(self, f, copy=True):
        if copy:
            shutil.copyfile(f, "{}/{}.json".format(self.folder, self.arduino))
            os.chmod("{}/{}.json".format(self.folder, self.arduino), 0o777)

        print("Reading config file...")
        fi = open(f)
        file_text = fi.read()
        json_data = json.loads(file_text)

        #Split into levels based on dependencies
        device_type = []
        current_search_path = CURRENT_DIR + "/appendages/"
        current_import_path = "appendages"
        current_depth_index = 0
        while True:
            file_list = [f for f in os.listdir(current_search_path)
                if os.path.isfile(current_search_path + f) and f[-3:] == ".py" and not f == "__init__.py"]
            device_type.append({})
            for f in file_list:
                module = importlib.import_module("{}.{}".format(current_import_path, f[:-3]))
                class_ = getattr(module, f[:-3])
                device_type[current_depth_index][f[:-7]] = class_()
            dir_list = [f for f in os.listdir(current_search_path) if os.path.isdir(current_search_path + f)]
            if len(dir_list) == 0:
                break
            current_search_path += dir_list[0] + "/"
            current_import_path += "." + dir_list[0]
            current_depth_index += 1

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
                elif json_item['type'] == 'velocityControlledMotor':
                    self.device_dict[json_item['type']].add(json_item, self.device_dict['motor'], self.device_dict['i2cencoder'] if 'i2cencoder' in self.device_dict else None, self.device_dict['encoder'] if 'encoder' in self.device_dict else None, self.device_dict['pid'])
                elif json_item['type'] == 'fourWheelDriveBase':
                    self.device_dict[json_item['type']].add(json_item, self.device_dict['motor'], self.device_dict['velocityControlledMotor'])
                else:
                    self.device_dict[json_item['type']].add(json_item)
        fi.close()
        print("Done")

    def generateOutput(self):
        if not hasattr(self, 'folder'):
            print("Parent folder has not been set")
            sys.exit()
        elif not hasattr(self, 'device_dict'):
            print("Config file has not been read")
            sys.exit()

        print("Generating output...")
        fo = open("{}/src/{}.ino".format(self.folder, self.arduino), 'w')
        gen = Generator(self.device_dict)
        print("\tWriting headers")
        fo.write(gen.add_header())
        print("\tWriting includes")
        fo.write(gen.add_includes())
        print("\tWriting pins")
        fo.write(gen.add_pins())
        print("\tWriting constructors")
        fo.write(gen.add_constructors())
        print("\tWriting setup")
        fo.write(gen.add_setup())
        print("\tWriting loop")
        fo.write(gen.add_loop())
        print("\tWriting parse args")
        fo.write(gen.add_parse_args())
        print("\tWriting check input")
        fo.write(gen.add_check_input())
        print("\tWriting parse and execute command")
        fo.write(gen.add_parse_and_execute_command_beginning())
        fo.write(gen.add_commands())
        fo.write(gen.add_parse_and_execute_command_ending())
        print("\tWriting extra functions")
        fo.write(gen.add_extra_functions())
        fo.write("\n")
        fo.close()
        os.chmod("{}/src/{}.ino".format(self.folder, self.arduino), 0o777)

        print("\tWriting indices file")
        gen.write_indices_file(self.folder, self.arduino)

        print("\tWriting build, serial, and upload shell scripts")
        gen.write_shell_scripts(self.folder, self.arduino)
        print("Done")
        print("Your output can be found at {}".format(self.folder))


    def build(self):
        if not hasattr(self, 'folder'):
            print("Parent folder has not been set")
            sys.exit()
        print("Building...")
        os.chdir("{}/{}".format(self.folder, self.arduino))
        os.system("ino build")
        print("Done")

    def upload(self):
        if not hasattr(self, 'folder'):
            print("Parent folder has not been set")
            sys.exit()
        print("Uploading...")
        ino_ini = open("{}{}/ino.ini".format(CURRENT_ARDUINO_CODE_DIR, self.arduino), 'r')
        ino_ini_text = ino_ini.read()
        shutil.rmtree("{}{}".format(CURRENT_ARDUINO_CODE_DIR, self.arduino))
        shutil.copytree(self.folder, "{}{}".format(CURRENT_ARDUINO_CODE_DIR, self.arduino))
        ino_ini = open("{}{}/ino.ini".format(CURRENT_ARDUINO_CODE_DIR, self.arduino), 'w')
        ino_ini.write(ino_ini_text)
        os.chmod("{}{}/ino.ini".format(CURRENT_ARDUINO_CODE_DIR, self.arduino), 0o777)
                
        os.chdir("{}{}".format(CURRENT_ARDUINO_CODE_DIR, self.arduino))
        os.system("sh upload.sh")
        print("Done")

if __name__ == "__main__":
    confFolder = "./conf"
    confFolderAbsPath = os.path.abspath(confFolder)
    deviceJsonFile = confFolderAbsPath + "/mega.json"
    ag = ArduinoGen(arduino="mega")
    ag.setParentFolder(os.path.dirname(os.path.realpath(__file__)))
    ag.setupFolder()
    ag.readConfig(deviceJsonFile)
    ag.generateOutput()
    ag.upload()
