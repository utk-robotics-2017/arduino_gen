from appendages.component_list import ComponentList


class FourWheelDrive:
    def __init__(self, label, useVelocityControl, lf_motor, rf_motor, lb_motor, rb_motor):
        self.label = label
        self.lf_motor = lf_motor
        self.rf_motor = rf_motor
        self.lb_motor = lb_motor
        self.rb_motor = rb_motor
        self.useVelocityControl = useVelocityControl


class FourWheelDriveList(ComponentList):
    TIER = 3

    def __init__(self):
        self.drive_list = []

    def add(self, json_item, motors, vcms):
        useVelocityControl = json_item['useVelocityControl']

        if useVelocityControl:
            lf_motor = vcms.get(json_item['leftFrontDriveMotor'])
            rf_motor = vcms.get(json_item['rightFrontDriveMotor'])
            lb_motor = vcms.get(json_item['leftBackDriveMotor'])
            rb_motor = vcms.get(json_item['rightBackDriveMotor'])
        else:
            lf_motor = motors.get(json_item['leftFrontDriveMotor'])
            rf_motor = motors.get(json_item['rightFrontDriveMotor'])
            lb_motor = motors.get(json_item['leftBackDriveMotor'])
            rb_motor = motors.get(json_item['rightBackDriveMotor'])

        self.drive_list.append(FourWheelDrive(json_item['label'], useVelocityControl, lf_motor,
                                              rf_motor, lb_motor, rb_motor))

    def get_includes(self):
        return '#include "FourWheelDrive.h"'

    def get_constructor(self):
        rv = "FourWheelDrive fwds[] = {\n"
        for drivebase in self.drive_list:
            if drivebase.useVelocityControl:
                rv += ("\tFourWheelDrive(&vcms[{0:s}_index], &vcms[{1:s}_index], " +
                       "&vcms[{2:s}_index], &vcms[{3:s}_index]),\n")\
                        .format(drivebase.lf_motor.label, drivebase.rf_motor.label,
                                drivebase.lb_motor.label, drivebase.rb_motor.label)
            else:
                rv += ("\tFourWheelDrive(&motors[{0:s}_index], &motors[{1:s}_index], " +
                       "&motors[{2:s}_index], &motors[{3:s}_index]),\n")\
                        .format(drivebase.lf_motor.label, drivebase.rf_motor.label,
                                drivebase.lb_motor.label, drivebase.rb_motor.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_commands(self):
        rv = "\tkDriveFWD,\n"
        rv += "\tkStopFWD,\n"
        rv += "\tkDriveFWD_PID,\n"
        rv += "\tkGetFWDLeftVelocity,\n"
        rv += "\tkGetFWDRightVelocity,\n"
        rv += "\tkGetFWDLeftPosition,\n"
        rv += "\tkGetFWDRightPosition,\n"
        return rv

    def get_command_attaches(self):
        rv = "\tcmdMessenger.attach(kDriveFWD, driveFWD);\n"
        rv += "\tcmdMessenger.attach(kStopFWD, stopFWD);\n"
        rv += "\tcmdMessenger.attach(kDriveFWD_PID, driveFWD_PID);\n"
        rv += "\tcmdMessenger.attach(kGetFWDLeftVelocity, getFWDLeftVelocity)\n"
        rv += "\tcmdMessenger.attach(kGetFWDRightVelocity, getFWDRightVelocity)\n"
        rv += "\tcmdMessenger.attach(kGetFWDLeftPosition, getFWDLeftPosition)\n"
        rv += "\tcmdMessenger.attach(kGetFWDRightPosition, getFWDRightPosition)\n"
        return rv

    def get_command_functions(self):
        rv = "void driveFWD() {\n"
        rv += "\tif(cmdMessenger.available()) {\n"
        rv += "\t\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\t\tif(indexNum < 0 || index > {0:d}) {{\n".format(len(self.drive_list))
        rv += '\t\t\tcmdMessenger.sendBinCmd(kError, kDriveFWD)\n'
        rv += "\t\t\treturn;\n"
        rv += "\t\t}\n"
        rv += "\t\tint values[4];\n:
        rv += "\t\tfor(int i = 0; i < 4; i++) {\n"
        rv += "\t\t\tif(cmdMessenger.available()) {\n"
        rv += "\t\t\t\tvalues[i] = cmdMessenger.readBinArg<int>();\n"
        rv += "\t\t\t\tif(values[i] < -1023 || values[i] > 1023)\n"
        rv += "\t\t\t\t\tcmdMessenger.sendBinCmd(kError, kDriveFWD);\n"
        rv += "\t\t\t\t\treturn;\n"
        rv += "\t\t\t\t}\n"
        rv += "\t\t\t} else {\n"
        rv += '\t\t\t\tcmdMessenger.sendBinCmd(kError, kDriveFWD);\n'
        rv += "\t\t\t\treturn;\n"
        rv += "\t\t\t}\n"
        rv += "\t\t}\n"
        rv += "\t\tfwds[indexNum].drive(values[0], values[1], values[2]], values[3]);\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kAcknowledge, kDriveFWD);\n"
        rv += "\t} else {\n"
        rv += '\t\tcmdMessenger.sendBinCmd(kError, kDriveFWD);\n'
        rv += "\t}\n
        rv += "}\n\n"

        rv += "void stopFWD() {\n"
        rv += "\tif(cmdMessenger.available()) {\n"
        rv += "\t\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\t\tif(indexNum < 0 || index > {0:d}) {{\n".format(len(self.drive_list))
        rv += '\t\t\tcmdMessenger.sendBinCmd(kError, kStopFWD)\n'
        rv += "\t\t\treturn;\n"
        rv += "\t\t}\n"
        rv += "\t\tfwds[indexNum].stop();\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kAcknowledge, kStopFWD);\n"
        rv += "\t} else {\n"
        rv += '\t\tcmdMessenger.sendBinCmd(kError, kStopFWD);\n'
        rv += "\t}\n
        rv += "}\n\n"

        rv += "void driveFWD_PID() {\n"
        rv += "\tif(cmdMessenger.available()) {\n"
        rv += "\t\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\t\tif(indexNum < 0 || index > {0:d}) {{\n".format(len(self.drive_list))
        rv += '\t\t\tcmdMessenger.sendBinCmd(kError, kDriveFWD_PID)\n'
        rv += "\t\t\treturn;\n"
        rv += "\t\t}\n"
        rv += "\t\tfloat values[4];\n:
        rv += "\t\tfor(int i = 0; i < 4; i++) {\n"
        rv += "\t\t\tif(cmdMessenger.available()) {\n"
        rv += "\t\t\t\tvalues[i] = cmdMessenger.readBinArg<int>();\n"
        rv += "\t\t\t} else {\n"
        rv += '\t\t\t\tcmdMessenger.sendBinCmd(kError, kDriveFWD_PID);\n'
        rv += "\t\t\t\treturn;\n"
        rv += "\t\t\t}\n"
        rv += "\t\t}\n"
        rv += "\t\tfwds[indexNum].drivePID(values[0], values[1], values[2]], values[3]);\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kAcknowledge, kDriveFWD_PID);\n"
        rv += "\t} else {\n"
        rv += '\t\tcmdMessenger.sendBinCmd(kError, kDriveFWD_PID);\n'
        rv += "\t}\n
        rv += "}\n\n"

        rv += "void getFWDLeftVelocity() {\n"
        rv += "\tif(cmdMessenger.available()) {\n"
        rv += "\t\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\t\tif(indexNum < 0 || index > {0:d}) {{\n".format(len(self.drive_list))
        rv += '\t\t\tcmdMessenger.sendBinCmd(kError, kGetFWDLeftVelocity)\n'
        rv += "\t\t\treturn;\n"
        rv += "\t\t}\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kAcknowledge, kGetFWDLeftVelocity);\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kResult, fwds[indexNum].getLeftVelocity());\n"
        rv += "\t} else {\n"
        rv += '\t\tcmdMessenger.sendBinCmd(kError, kGetFWDLeftVelocity);\n'
        rv += "\t}\n
        rv += "}\n\n"

        rv += "void getFWDRightVelocity() {\n"
        rv += "\tif(cmdMessenger.available()) {\n"
        rv += "\t\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\t\tif(indexNum < 0 || index > {0:d}) {{\n".format(len(self.drive_list))
        rv += '\t\t\tcmdMessenger.sendBinCmd(kError, kGetFWDRightVelocity)\n'
        rv += "\t\t\treturn;\n"
        rv += "\t\t}\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kAcknowledge, kGetFWDRightVelocity);\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kResult, fwds[indexNum].getRightVelocity());\n"
        rv += "\t} else {\n"
        rv += '\t\tcmdMessenger.sendBinCmd(kError, kGetFWDRightVelocity);\n'
        rv += "\t}\n
        rv += "}\n\n"

        rv += "void getFWDLeftPosition) {\n"
        rv += "\tif(cmdMessenger.available()) {\n"
        rv += "\t\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\t\tif(indexNum < 0 || index > {0:d}) {{\n".format(len(self.drive_list))
        rv += '\t\t\tcmdMessenger.sendBinCmd(kError, kGetFWDLeftPosition)\n'
        rv += "\t\t\treturn;\n"
        rv += "\t\t}\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kAcknowledge, kGetFWDLeftPosition);\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kResult, fwds[indexNum].getLeftPosition());\n"
        rv += "\t} else {\n"
        rv += '\t\tcmdMessenger.sendBinCmd(kError, kGetFWDLeftPosition);\n'
        rv += "\t}\n
        rv += "}\n\n"

        rv += "void getFWDRightPosition() {\n"
        rv += "\tif(cmdMessenger.available()) {\n"
        rv += "\t\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\t\tif(indexNum < 0 || index > {0:d}) {{\n".format(len(self.drive_list))
        rv += '\t\t\tcmdMessenger.sendBinCmd(kError, kGetFWDRightPosition)\n'
        rv += "\t\t\treturn;\n"
        rv += "\t\t}\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kAcknowledge, kGetFWDRightPosition);\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kResult, fwds[indexNum].getRightPosition());\n"
        rv += "\t} else {\n"
        rv += '\t\tcmdMessenger.sendBinCmd(kError, kGetFWDRightPosition);\n'
        rv += "\t}\n
        rv += "}\n\n"

        return rv

    def get_core_values(self):
        for i, drivebase in enumerate(self.drive_list):
            a = {}
            a['index'] = i
            a['label'] = drivebase['label']
            a['useVelocityControl'] = drivebase.useVelocityControl
            yield a
