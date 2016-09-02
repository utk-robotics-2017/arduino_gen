# ArduinoGen
ArduinoGen is a program that using a configuration file containing all the appendages (sensors, actuators, systems) connected to the Arduino, writes Arduino code that works with the call-response nature of RIP's spine core.

## [Web Interface](https://utk-robotics-2017.github.io/ArduinoGen/index.html)
[source](https://github.com/utk-robotics-2017/utk-robotics-2017.github.io/tree/master/ArduinoGen)

The web interface allows the generation of the config file by dragging appendages into the list and setting their various parameters. If one of the raspberry pi's is running the server then it can be connected to and config files can be retrieved, posted to the pi, or written to the Arduino.

## Backend

The backend of ArduinoGen works with the server, but also be included as a class into any python script as well as run via command line. This class generates the arduino code, and indices config file for RIP's spine core, a build script, a serial com script, and an upload script.

### Usage
```

usage: ArduinoGen.py [-h] -a ARDUINO -pf PARENT_FOLDER -c CONFIG [-b BUILD] [-u UPLOAD]

optional arguments:
  -h, --help            show this help message and exit
  -a ARDUINO, --arduino ARDUINO
                        Name of the arduino
  -pf PARENT_FOLDER, --parent_folder PARENT_FOLDER
                        Parent folder of the folder to put all the output
                        files
  -c CONFIG, --config CONFIG
                        Location of the config json file
  -b BUILD, --build BUILD
                        Build the ino file into something that can be uploaded
                        to the Arduino
  -u UPLOAD, --upload UPLOAD
                        Build the ino file and upload that onto the Arduino

```

## Current Arduino Code
The current code on the Arduino is contained in the currentArduinoCode folder which should be in the root directory and a commit is made each time new Arduino code is put on an Arduino.

## Arduino Libraries
All libraries that are to be used with the Arduino Code should be in ArduinoLibraries which should be in the root directory.

## Building and Uploading
Building and uploading use a modified version of the ino library. Our modification cause the library to check the ArduinoLibraries folder for includes.

## Serial Communication
Currently, we are using picocom to manually communicate with the Arduino. Ctrl-X, Ctrl-A is how you exit.
However, we are working on ArduinoCom as a replacement to picocom.
