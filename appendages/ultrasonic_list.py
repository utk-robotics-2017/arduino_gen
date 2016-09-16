from appendages.component_list import ComponentList


class Ultrasonic:
    def __init__(self, label, pin):
        self.label = label
        self.pin = pin


class UltrasonicList(ComponentList):
    TIER = 1

    def __init__(self):
        self.sensor_list = []

    def add(self, json_item):
        self.sensor_list.append(Ultrasonic(json_item['label'], json_item['pin']))

    def get_includes(self):
        return '#include "NewPing.h"\n'

    def get_pins(self):
        rv = ""
        for sensor in self.sensor_list:
            rv += "const char {0:s}_pin = {1:d};\n".format(sensor.label, sensor.pin)
        rv += "\n"
        return rv

    def get_constructor(self):
        rv = ""
        for i, sensor in enumerate(self.sensor_list):
            rv += "const char {0:s}_index = {1:d};\n".format(sensor.label, i)
        rv += "NewPing ultrasonics[{0:d}] = {{\n".format(len(self.sensor_list))

        for sensor in self.sensor_list:
            rv += "\tNewPing({0:s}_pin, {0:s}_pin),\n".format(sensor.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_commands(self):
        return "kReadUltrasonic,\n\t"

    def get_command_attaches(self):
        return "\tcmdMessenger.attach(kReadUltrasonic, readUltrasonic);\n"

    def get_command_functions(self):
        rv = "void readUltrasonic() {\n"
        rv += "\tif(cmdMessenger.available()) {\n"
        rv += "\t\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\t\tif(indexNum < 0 || index > {0:d}) {{\n".format(len(self.sensor_list))
        rv += '\t\t\tcmdMessenger.sendBinCmd(kError, kReadUltrasonic)\n'
        rv += "\t\t\treturn;\n"
        rv += "\t\t}\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kAcknowledge, kReadUltrasonic);\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kResult, ultrasonics[indexNum].ping());\n"
        rv += "\t} else {\n"
        rv += '\t\tcmdMessenger.sendBinCmd(kError, kReadUltrasonic);\n'
        rv += "\t}\n
        rv += "}\n\n"

    def get_core_values(self):
        for i, ultrasonic in enumerate(self.sensor_list):
            a = {}
            a['index'] = i
            a['label'] = ultrasonic['label']
            yield a
