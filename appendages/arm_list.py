from appendages.component_list import ComponentList


class Arm:
    def __init__(self, label, base, shoulder, elbow, wrist, wrist_rotate):
        self.label = label
        self.base = base
        self.shoulder = shoulder
        self.elbow = elbow
        self.wrist = wrist
        self.wrist_rotate = wrist_rotate


class ArmList(ComponentList):
    TIER = 2

    def __init__(self):
        self.arm_list = []

    def add(self, json_item, servos):

        base_servo = servos.get(json_item['base_label'])
        shoulder_servo = servos.get(json_item['shoulder_label'])
        elbow_servo = servos.get(json_item['elbow_label'])
        wrist_servo = servos.get(json_item['wrist_label'])
        wrist_rotate_servo = servos.get(json_item['wrist_rotate_label'])

        self.arm_list.append(Arm(json_item['label'], base_servo, shoulder_servo, elbow_servo,
                                 wrist_servo, wrist_rotate_servo))

    def get_includes(self):
        return '#include "Arm.h";\n'

    def get_constructor(self):
        rv = "Arm arms[{0:d}] = {{\n".format(len(self.arm_list))
        for arm in self.arm_list:
            rv += ("\tArm({0:s}_index, {1:s}_index, {2:s}_index, {3:s}_index, {4:s}_index, " +
                   "servo_pins, servos),\n").format(arm.base.label, arm.shoulder.label,
                                                    arm.elbow.label, arm.wrist.label,
                                                    arm.wrist_rotate.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_commands(self):
        return "\tkSetArm,\n\tkDetachArm,\n"

    def get_command_attaches(self):
        rv = "\tcmdMessenger.attach(kSetArm, setArm);\n"
        rv += "\tcmdMessenger.attach(kDetachArm, detachArm);\n"
        return rv

    def get_command_functions(self):
        rv = "void setArm() {\n"
        rv += "\tif(cmdMessenger.available()) {\n"
        rv += "\t\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\t\tif(indexNum < 0 || index > {0:d}) {{\n".format(len(self.arm_list))
        rv += '\t\t\tcmdMessenger.sendBinCmd(kError, kSetArm)\n'
        rv += "\t\t\treturn;\n"
        rv += "\t\t}\n"
        rv += "\t\tint pos[5];\n:
        rv += "\t\tfor(int i = 0; i < 5; i++) {\n"
        rv += "\t\t\tif(cmdMessenger.available()) {\n"
        rv += "\t\t\t\tpos[i] = cmdMessenger.readBinArg<int>();\n"
        rv += "\t\t\t} else {\n"
        rv += '\t\t\t\tcmdMessenger.sendBinCmd(kError, kSetArm);\n'
        rv += "\t\t\t\treturn;\n"
        rv += "\t\t\t}\n"
        rv += "\t\t}\n"
        rv += "\t\tarms[indexNum].set(pos[0], pos[1], pos[2]], pos[3], pos[4]);\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kAcknowledge, kSetArm);\n"
        rv += "\t} else {\n"
        rv += '\t\tcmdMessenger.sendBinCmd(kError, kSetArm);\n'
        rv += "\t}\n
        rv += "}\n\n"
        rv += "void detachArm() {\n"
        rv += "\tif(cmdMessenger.available()) {\n"
        rv += "\t\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\t\tif(indexNum < 0 || index > {0:d}) {{\n".format(len(self.arm_list))
        rv += '\t\t\tcmdMessenger.sendBinCmd(kError, kDetachArm)\n'
        rv += "\t\t\treturn;\n"
        rv += "\t\t}\n"
        rv += "\t\tarms[indexNum].detach();\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kAcknowledge, kDetachArm);\n"
        rv += "\t} else {\n"
        rv += '\t\tcmdMessenger.sendBinCmd(kError, kDetachArm);\n'
        rv += "\t}\n
        rv += "}\n\n"
        return rv

    def get_core_values(self):
        for i, arm in enumerate(self.arm_list):
            a = {}
            a['index'] = i
            a['label'] = arm['label']
            yield a
