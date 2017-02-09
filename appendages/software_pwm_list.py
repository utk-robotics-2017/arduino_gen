from appendages.component_list import ComponentList


class SoftwarePWM:
    def __init__(self, label, pin):
        self.label = label
        self.pin = pin


class SoftwarePwmList(ComponentList):
    TIER = 1

    def __init__(self):
        self.list_ = []

    def add(self, json_item):
        self.list_.append(SoftwarePWM(json_item['label'], json_item['pin']))

    def get_include(self):
        return "#include <SoftPWM.h>"

    def get_pins(self):
        rv = "int[] software_pwm_pin = {\n"
        for pwm in self.list_:
            rv += "\t{0:d}\n".format(pwm.pin)
        rv += "}\n"

    def get_setup(self):
        rv = "\tSoftPWMBegin();\n"
        for pwm in self.list_:
            rv += "\tSoftPWMSet({0:d}, 0);".format(pwm.pin)
        return rv

    def get_commands(self):
        return "\tkSetPWM,\n"

    def get_command_attaches(self):
        return "\tcmdMessenger.attach(kSetPWM, setPWM);\n"

    def get_command_functions(self):
        rv = "void setPWM(){\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.list_))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kReadEncoder);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tint value = cmdMessenger.readBinArg<int>();\n"
        rv += "\tSoftPWM(software_pwm_pin[indexNum], value);\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kSetPWM);\n"
        rv += "}\n\n"

    def get_indices(self):
        for i, pwm in enumerate(self.list_):
            yield i, pwm

    def get_core_values(self):
        for i, pwm in enumerate(self.list_):
            a = {}
            a['index'] = i
            a['label'] = pwm.label
            a['type'] = "SoftwarePwm"
            yield a
