import argparse
import json
import os
import shutil
import sys
import importlib

from generator import Generator

from appendages.utils.logger import Logger
logger = Logger()

# Import all the files in appendages
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
CURRENT_ARDUINO_CODE_DIR = "/Robot/CurrentArduinoCode"


class ArduinoGen:
    def __init__(self, arduino):
        self.arduino = arduino

    def setParentFolder(self, parentFolder):
        self.folder = "{0:s}/{1:s}".format(parentFolder, self.arduino)

    def setupFolder(self):
        if not hasattr(self, 'folder'):
            print("Folder has not been set")
            sys.exit()
        logger.info("Making directory...")
        if os.path.exists(self.folder):
            shutil.rmtree(self.folder)
        os.makedirs(self.folder, 0o777)
        os.chmod(self.folder, 0o777)
        os.makedirs("{0:s}/src".format(self.folder), 0o777)
        os.chmod("{0:s}/src".format(self.folder), 0o777)
        logger.info("Done")

    def readConfig(self, f, copy=True):
        if copy:
            shutil.copyfile(f, "{0:s}/{1:s}.json".format(self.folder, self.arduino))
            os.chmod("{0:s}/{1:s}.json".format(self.folder, self.arduino), 0o777)

        logger.info("Reading config file...")
        with open(f) as fi:
            file_text = fi.read()
        json_data = json.loads(file_text)

        # Split into levels based on dependencies
        device_type = []
        current_search_path = CURRENT_DIR + "/appendages/arduino_gen/"
        current_import_path = "appendages.arduino_gen."
        file_list = []
        # Grab all appendage files from directory
        for f in os.listdir(current_search_path):
            if os.path.isfile(current_search_path + f) and f[-3:] == ".py" and not f == "__init__.py":
                file_list.append(f)

        class_dict = {}
        device_dict = {}
        for f in file_list:
            logger.info("Module: {0:s}.{1:s}".format(current_import_path, f[:-3]))
            module = importlib.import_module("{0:s}.{1:s}".format(current_import_path, f[:-3]))
            class_name = f[:-3].replace('_', ' ').title().replace(' ', '')
            logger.info("Class: {0:s}".format(class_name))
            class_ = getattr(module, class_name)
            class_dict[class_name] = class_

        for json_item in json_data:
            if json_item['type'].lower() in ['limit_switch', 'button']:
                json_item['type'] = 'DigitalInput'

            if json_item['type'].lower() in ['led']:
                json_item['type'] = 'DigitalOutput'

            if json_item['type'] not in device_dict:
                device_dict[json_item['type']] = []

            device_dict[json_item['type']].append(class_dict[json_item['type']](json_item=json_item, class_dict=class_dict, device_dict=device_dict))

        logger.info("Done")

    def generateOutput(self):
        if not hasattr(self, 'folder'):
            logger.error("Parent folder has not been set")
            sys.exit()
        elif not hasattr(self, 'device_dict'):
            logger.error("Config file has not been read")
            sys.exit()

        logger.info("Generating output...")
        with open("{0:s}/src/{1:s}.ino".format(self.folder, self.arduino), 'w') as fo:
            generator = Generator(self.device_dict)
            logger.write("\tLoading templates... [{0:s}] 0/{1:d}".format(' ' * 20, len(self.device_dict)), repeated=True)
            generator.load_templates()
            logger.info("\tWriting file... [{0:s}] 0/10".format(' ' * 10), repeated=True)
            generator.write_file(fo)
        os.chmod("{0:s}/src/{1:s}.ino".format(self.folder, self.arduino), 0o777)

        logger.info("\tWriting indices file")
        generator.write_core_config_file(self.folder, self.arduino)

        logger.info("\tWriting build, serial, and upload shell scripts")
        generator.write_shell_scripts(self.folder, self.arduino)
        logger.info("Done")
        logger.info("Your output can be found at {0:s}".format(self.folder))

    def build(self):
        if not hasattr(self, 'folder'):
            logger.error("Parent folder has not been set")
            sys.exit()
        logger.info("Building...")
        os.chdir("{0:s}/{1:s}".format(self.folder, self.arduino))
        os.system("ino build")
        logger.info("Done")

    def upload(self):
        if not hasattr(self, 'folder'):
            logger.error("Parent folder has not been set")
            sys.exit()
        logger.info("Uploading...")

        with open("{0:s}/{1:s}/platformio.ini".format(CURRENT_ARDUINO_CODE_DIR, self.arduino), 'r') as pio_ini:
            pio_ini_text = pio_ini.read()
        shutil.rmtree("{0:s}/{1:s}".format(CURRENT_ARDUINO_CODE_DIR, self.arduino))
        logger.info("Copying {0:s} to {1:s}/{2:s}".format(self.folder, CURRENT_ARDUINO_CODE_DIR,
                                                          self.arduino))
        shutil.copytree(self.folder, "{0:s}/{1:s}".format(CURRENT_ARDUINO_CODE_DIR, self.arduino))
        with open("{0:s}/{1:s}/platformio.ini".format(CURRENT_ARDUINO_CODE_DIR, self.arduino), 'w') as pio_ini:
            pio_ini.write(pio_ini_text)
        os.chmod("{0:s}/{1:s}/platformio.ini".format(CURRENT_ARDUINO_CODE_DIR, self.arduino), 0o777)

        logger.info("You have moved to {0:s}/{1:s}".format(CURRENT_ARDUINO_CODE_DIR, self.arduino))
        os.chdir("{0:s}/{1:s}".format(CURRENT_ARDUINO_CODE_DIR, self.arduino))
        logger.info(os.getcwd())
        os.system("sh upload.sh")
        # os.system("pio run -t upload")
        print("Done")


if __name__ == "__main__":
    # Collect command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--arduino", required=True, help="Name of the arduino")
    ap.add_argument("-pf", "--parent_folder", required=True,
                    help="Parent folder of the folder to put all the output files")
    ap.add_argument("-c", "--config", required=True, help="Location of the config json file")
    ap.add_argument("-b", "--build", required=False,
                    help="Build the ino file into something that can be uploaded to the arduino")
    ap.add_argument("-u", "--upload", required=False, help="Build the ino file and upload that on to the arduino")
    args = vars(ap.parse_args())

    # TODO: Add creating lock file

    ag = ArduinoGen(args['arduino'])
    ag.setParentFolder(args['parent_folder'])
    ag.readConfig(args['config'])
    ag.generateOutput()

    if args['upload']:
        ag.upload()
    elif args['build']:
        ag.build()
