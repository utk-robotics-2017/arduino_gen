# ArduinoGen
Arduino Code Generator for the UTK IEEE Robotics Integrated Platform (RIP)


## [Front End](https://utk-robotics-2017.github.io/ArduinoGen/index.html)
A web interface that allows the user to input what sensors, actuators, and systems they want connected to their arduino, what pins are being used, and any other information specific to the sensors, actuators, or systems selected. A configuration file (in json) is created based on the inputs.

## Back End
The configuration file is then used to autogenerate Arduino code that supports the command response system implemented by the UTK IEEE Robot Team's Robotics Integrated Platform.

python ArduinoGen.py -a <arduino> -at <arduino-type> -pf <parent folder> -c <config file> [-b <build>] [-u <upload>]
