from appendages.component_list import ComponentList


class Motor:
    def __init__(self, label, inA_pin, inB_pin, pwm_pin, reverse, motor_controller):
        self.label = label
        self.inA_pin = inA_pin
        self.inB_pin = inB_pin
        self.pwm_pin = pwm_pin
        self.reverse = reverse
        self.motor_controller = motor_controller


class MotorList(ComponentList):
    TIER = 1

    def __init__(self):
        self.motorDict = {}
        self.motorList = []

    def add(self, json_item):
        if json_item['motorController'].lower() == 'monstermoto':
            motor = Motor(json_item['label'], json_item['inA_pin'], json_item['inB_pin'],
                          json_item['pwm_pin'], json_item['reverse'], 'MonsterMoto')
        elif json_item['motorController'].lower() == 'roverfive':
            motor = Motor(json_item['label'], json_item['dir_pin'], -1, json_item['pwm_pin'],
                          json_item['reverse'], 'RoverFive')

        self.motorDict[motor.label] = motor
        self.motorList.append(motor)
        self.motorList.sort(key=lambda x: x.label, reverse=False)

    def get(self, label):
        if label in self.motorDict:
            return self.motorDict[label]
        else:
            return None

    def get_includes(self):
        return '#include "Motor.h"\n'

    def get_pins(self):
        rv = ""
        for motor in self.motorList:
            rv += "const char {0:s}_Apin = {1:d};\n".format(motor.label, motor.inA_pin)
            rv += "const char {0:s}_Bpin = {1:d};\n".format(motor.label, motor.inB_pin)
            rv += "const char {0:s}_PWMpin = {1:d};\n".format(motor.label, motor.pwm_pin)
        return rv

    def get_constructor(self):
        rv = ""
        for i, motor in enumerate(self.motorList):
            rv += "const char {0:s}_index = {1:d};\n".format(motor.label, i)
        rv += "Motor motors[{0:d}] = {{\n".format(len(self.motorList))
        for motor in self.motorList:
            rv += "\tMotor({0:s}_Apin, {0:s}_Bpin, {0:s}_PWMpin, {1:d}, {2:s}),\n"\
                    .format(motor.label, 1 if motor.reverse else 0,
                            motor.motor_controller)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        rv = ""
        for motor in self.motorList:
            rv += "\tpinMode({0:s}_Apin, OUTPUT);\n".format(motor.label)
            if not motor.inB_pin == -1:
                rv += "\tpinMode({0:s}_Bpin, OUTPUT);\n".format(motor.label)
            rv += "\tpinMode({0:s}_PWMpin, OUTPUT);\n".format(motor.label)
        return rv

    def get_commands(self):
        return "\tkDriveMotor,\n\tkStopMotor,\n"

    def get_command_attaches(self):
        rv = "\tcmdMessenger.attach(kDriveMotor, driveMotor);\n"
        rv += "\tcmdMessenger.attach(kStopMotor, stopMotor);\n"
        return rv

    def get_command_functions(self):
        rv = "void driveMotor() {\n"
        rv += "\tint indexNum = cmdMessenger.readInt16Arg();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.motorList))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kDriveMotor);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tint value = cmdMessenger.readInt16Arg();\n"
        rv += "\tif(cmdMessenger.isArgOk() && value > -1024 && value < 1024) {\n"
        rv += "\t\tmotors[indexNum].drive(value);\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kAcknowledge, kDriveMotor);\n"
        rv += "\t} else {\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kDriveMotor);\n"
        rv += "\t}\n"
        rv += "}\n\n"

        rv += "void stopMotor() {\n"
        rv += "\tint indexNum = cmdMessenger.readInt16Arg();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.motorList))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kStopMotor);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tmotors[indexNum].stop();\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kStopMotor);\n"
        rv += "}\n\n"
        return rv

    def get_core_values(self):
        for i, motor in enumerate(self.motorList):
            a = {}
            a['index'] = i
            a['label'] = motor.label
            a['type'] = "Motor"
            yield a
