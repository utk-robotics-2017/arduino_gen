from appendages.component_list import ComponentList


class EasyStepper:
    def __init__(self, label, steps, dir_pin, step_pin, initial_speed):
        self.label = label
        self.steps = steps
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        self.initial_speed = initial_speed
        self.angle_per_step = 360.0 / steps  # maybe change


class EasyStepperList(ComponentList):
    TIER = 1

    def __init__(self):
        self.stepperDict = {}
        self.stepperList = []

    def add(self, json_item, device_dict, device_type):
        stepper = EasyStepper(json_item['label'], json_item['number_of_steps'],
                              json_item['dir_pin'], json_item['step_pin'],
                              json_item['initial_speed'])
        self.stepperDict[json_item['label']] = stepper
        self.stepperList.append(stepper)
        self.stepperList.sort(key=lambda x: x.label, reverse=False)

    def get(self, label):
        return self.actuators[label]

    def get_includes(self):
        return '#include "EasyDriver.h"\n'

    def get_pins(self):
        rv = ""
        for stepper in self.stepperList:
            rv += "const char {0:s}_dir_pin = {1:d};\n".format(stepper.label, stepper.dir_pin)
            rv += "const char {0:s}_step_pin = {1:d};\n".format(stepper.label, stepper.step_pin)
            rv += "const int {0:s}_init_speed = {1:d};\n".format(stepper.label, stepper.initial_speed)
        rv += "\n"
        return rv

    def get_constructor(self):
        rv = ""
        for i, stepper in enumerate(self.stepperList):
            rv += "const char {0:s}_index = {1:d};\n".format(stepper.label, i)

        rv += ("EasyStepper easySteppers[{0:d}] = {{\n").format(len(self.stepperList))
        for stepper in self.stepperList:
            rv += ("\tEasyStepper({0:d}, {1:s}_dir_pin, {1:s}_step_pin, {1:s}_init_speed),\n")\
                .format(stepper.steps, stepper.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        rv = ""
        for stepper in self.stepperList:
            rv += "\tpinMode({0:s}_dir_pin, OUTPUT);\n".format(stepper.label)
            rv += "\tpinMode({0:s}_step_pin, OUTPUT);\n".format(stepper.label)

        '''
        for stepper in self.stepperList:
            rv += ("\teasySteppers[{0:s}_index].setSpeed({1:d});\n").format(stepper.label,
                                                                            stepper.initial_speed)
        '''
        rv += "\n"

        return rv

    def get_commands(self):
        return "\tkEasySetStepperSpeed,\n\tkEasyStepAngle,\n\tkEasyStep,\n"

    def get_command_attaches(self):
        rv = "\tcmdMessenger.attach(kEasySetStepperSpeed, setSpeed);\n"
        rv += "\tcmdMessenger.attach(kEasyStepAngle, stepAng);\n"
        rv += "\tcmdMessenger.attach(kEasyStep, step);\n"
        return rv

    def get_command_functions(self):
        rv = "void setSpeed() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() ||indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.stepperList))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kEasySetStepperSpeed);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tint value = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk()){\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kEasySetStepperSpeed);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\teasySteppers[indexNum].setSpeed(value);\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kEasySetStepperSpeed);\n"
        rv += "}\n\n"

        rv += "void stepAng() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.stepperList))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kEasyStepAngle);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tint value = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk()){\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kEasyStepAngle);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\teasySteppers[indexNum].stepAng(value);\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kEasyStepAngle);\n"
        rv += "}\n\n"

        rv += "void step() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.stepperList))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kEasyStep);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tint value = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk()){\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kEasyStep);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\teasySteppers[indexNum].step(value);\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kEasyStep);\n"
        rv += "}\n\n"
        return rv

    def get_core_values(self):
        for i, stepper in enumerate(self.stepperList):
            config = {}
            config['index'] = i
            config['label'] = stepper.label
            config['type'] = "Easy Stepper"
            config['initial_speed'] = stepper.initial_speed
            config['angle_per_step'] = stepper.angle_per_step
            yield config
