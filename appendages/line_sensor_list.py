from appendages.component_list import ComponentList


class LineSensor:
    def __init__(self, label, pin):
        self.label = label
        self.pin = pin


class LineSensorList(ComponentList):
    TIER = 1

    def __init__(self):
        self.digital_sensor_list = []
        self.analog_sensor_list = []

    def add(self, json_item):
        if(json_item['digital']):
            self.digital_sensor_list.append(LineSensor(json_item['label'], json_item['pin']))
        else:
            self.analog_sensor_list.append(LineSensor(json_item['label'], json_item['pin']))

    def get_pins(self):
        rv = ""
        for sensor in self.digital_sensor_list:
            rv += "const char {0:s}_pin = {1:d};\n".format(sensor.label, sensor.pin)
        for sensor in self.analog_sensor_list:
            rv += "const char {0:s}_pin = {1:d};\n".format(sensor.label, sensor.pin)
        rv += "\n"
        return rv

    def get_constructor(self):
        rv = ""
        if(len(self.digital_sensor_list) > 0):
            for i, linesensor in enumerate(self.digital_sensor_list):
                rv += "const char {0:s}_index = {1:d};\n".format(linesensor.label, i)

            rv += "char digital_linesensors[{0:d}] = {{\n".format(len(self.digital_sensor_list))

            for sensor in self.digital_sensor_list:
                rv += ("\t{0:s}_pin,\n").format(sensor.label)

            rv = rv[:-2] + "\n};\n"

        if(len(self.analog_sensor_list) > 0):
            for i, linesensor in enumerate(self.analog_sensor_list):
                rv += "const char {0:s}_index = {1:d};\n".format(linesensor.label, i)

            rv += "char analog_linesensors[{0:d}] = {{\n".format(len(self.analog_sensor_list))

            for sensor in self.analog_sensor_list:
                rv += ("\t{0:s}_pin,\n").format(sensor.label)

            rv = rv[:-2] + "\n};\n"

        return rv

    def get_commands(self):
        rv = ""
        if(len(self.digital_sensor_list) > 0):
            rv += "\tkReadDigitalLineSensor,\n"
        if(len(self.analog_sensor_list) > 0):
            rv += "\tkReadAnalogLineSensor,\n"
        return rv

    def get_command_attaches(self):
        rv = ""
        if(len(self.digital_sensor_list) > 0):
            rv += "\tcmdMessenger.attach(kReadDigitalLineSensor, readDigitalLineSensor);\n"
        if(len(self.analog_sensor_list) > 0):
            rv += "\tcmdMessenger.attach(kReadAnalogLineSensor, readAnalogLineSensor);\n"
        return rv

    def get_command_functions(self):
        rv = ""
        if(len(self.digital_sensor_list) > 0):
            rv += "void readDigitalLineSensor() {\n"
            rv += "\tif(cmdMessenger.available()) {\n"
            rv += "\t\tint indexNum = cmdMessenger.readBinArg<int>();\n"
            rv += "\t\tif(indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.digital_sensor_list))
            rv += "\t\t\tcmdMessenger.sendBinCmd(kError, kReadDigitalLineSensor);\n"
            rv += "\t\t\treturn;\n"
            rv += "\t\t}\n"
            rv += "\t\tcmdMessenger.sendBinCmd(kAcknowledge, kReadDigitalLineSensor);\n"
            rv += "\t\tcmdMessenger.sendBinCmd(kResult, digitalRead(digital_linesensors[indexNum]));\n"
            rv += "\t} else {\n"
            rv += "\t\tcmdMessenger.sendBinCmd(kError, kReadDigitalLineSensor);\n"
            rv += "\t}\n"
            rv += "}\n\n"
        if(len(self.analog_sensor_list) > 0):
            rv += "void readAnalogLineSensor() {\n"
            rv += "\tif(cmdMessenger.available()) {\n"
            rv += "\t\tint indexNum = cmdMessenger.readBinArg<int>();\n"
            rv += "\t\tif(indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.analog_sensor_list))
            rv += "\t\t\tcmdMessenger.sendBinCmd(kError, kReadAnalogLineSensor);\n"
            rv += "\t\t\treturn;\n"
            rv += "\t\t}\n"
            rv += "\t\tcmdMessenger.sendBinCmd(kAcknowledge, kReadAnalogLineSensor);\n"
            rv += "\t\tcmdMessenger.sendBinCmd(kResult, analogRead(analog_linesensors[indexNum]));\n"
            rv += "\t} else {\n"
            rv += "\t\tcmdMessenger.sendBinCmd(kError, kReadAnalogLineSensor);\n"
            rv += "\t}\n"
            rv += "}\n\n"
        return rv

    def get_core_values(self):
        for i, linesensor in enumerate(self.digital_sensor_list):
            a = {}
            a['index'] = i
            a['label'] = linesensor.label
            a['digital'] = True
            yield a
        for i, linesensor in enumerate(self.analog_sensor_list):
            a = {}
            a['index'] = i
            a['label'] = linesensor.label
            a['digital'] = False
            yield a
