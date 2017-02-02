from appendages.component_list import ComponentList


class Switch:
    def __init__(self, label, pin, pullup):
        self.label = label
        self.pin = pin
        self.pullup = pullup


class SwitchList(ComponentList):
    TIER = 1

    def __init__(self):
        self.list_ = []

    def add(self, json_item, device_dict, device_type):
        switch = Switch(json_item['label'], json_item['pin'], json_item['pullup'])
        self.list_.append(switch)
        self.list_.sort(key=lambda x: x.label, reverse=False)
        return switch

    def get_pins(self):
        rv = ""
        for sensor in self.list_:
            rv += "const char {0:s}_pin = {1:d};\n".format(sensor.label, sensor.pin)
        rv += "\n"
        return rv

    def get_constructor(self):
        rv = ""
        for i, sensor in enumerate(self.list_):
            rv += "const char {0:s}_index = {1:d};\n".format(sensor.label, i)
        rv += "char switches[{0:d}] = {{\n".format(len(self.list_))
        for sensor in self.list_:
            rv += ("\t{0:s}_pin,\n").format(sensor.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        rv = ""
        for sensor in self.list_:
            if sensor.pullup:
                rv += "\tpinMode({0:s}_pin, INPUT_PULLUP);\n".format(sensor.label)
            else:
                rv += "\tpinMode({0:s}_pin, INPUT);\n".format(sensor.label)
        rv += "\n"
        return rv

    def get_commands(self):
        return "\tkReadSwitch,\n\tkReadSwitchResult,\n"

    def get_command_attaches(self):
        return "\tcmdMessenger.attach(kReadSwitch, readSwitch);\n"

    def get_command_functions(self):
        rv = "void readSwitch() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.list_))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kReadSwitch);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kAcknowledge, kReadSwitch);\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kReadSwitchResult, digitalRead(switches[indexNum]));\n"
        rv += "}\n\n"
        return rv

    def get_core_values(self):
        for i, switch in enumerate(self.list_):
            a = {}
            a['index'] = i
            a['label'] = switch.label
            a['type'] = "Switch"
            yield a
