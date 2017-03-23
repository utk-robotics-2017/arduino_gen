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
        self.list_ = []

    def add(self, json_item, device_dict, device_type):
        if 'servo' not in device_dict:
            for device_level in device_type:
                if 'servo' in device_level:
                    device_dict['servo'] = device_level['servo']
                    break

        base_servo = device_dict['servo'].add(json_item['base'], device_dict, device_type)
        shoulder_servo = device_dict['servo'].add(json_item['shoulder'], device_dict, device_type)
        elbow_servo = device_dict['servo'].add(json_item['elbow'], device_dict, device_type)
        wrist_servo = device_dict['servo'].add(json_item['wrist'], device_dict, device_type)
        wrist_rotate_servo = device_dict['servo'].add(json_item['wrist_rotate'],
                                                      device_dict, device_type)

        arm = Arm(json_item['label'], base_servo, shoulder_servo, elbow_servo,
                  wrist_servo, wrist_rotate_servo)

        self.list_.append(arm)

        return arm

    def get_includes(self):
        return '#include "Arm.h"\n'

    def get_constructors(self):
        rv = "Arm arms[{0:d}] = {{\n".format(len(self.list_))
        for arm in self.list_:
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
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.list_))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kSetArm);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tint pos[5];\n"
        rv += "\tfor(int i = 0; i < 5; i++) {\n"
        rv += "\t\tpos[i] = cmdMessenger.readBinArg<int>();\n"
        rv += "\t\tif(!cmdMessenger.isArgOk()){\n"
        rv += "\t\t\tcmdMessenger.sendBinCmd(kError, kSetArm);\n"
        rv += "\t\t\treturn;\n"
        rv += "\t\t}\n"
        rv += "\t}\n"
        rv += "\tarms[indexNum].set(pos[0], pos[1], pos[2], pos[3], pos[4]);\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kSetArm);\n"
        rv += "}\n\n"

        rv += "void detachArm() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.list_))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kDetachArm);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tarms[indexNum].detach();\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kDetachArm);\n"
        rv += "}\n\n"
        return rv

    def get_core_values(self):
        for i, arm in enumerate(self.list_):
            config = {}
            config['index'] = i
            config['type'] = "Arm"
            config['label'] = arm.label
            config['base'] = arm.base.label
            config['shoulder'] = arm.shoulder.label
            config['elbow'] = arm.elbow.label
            config['wrist'] = arm.wrist.label
            config['wrist_rot'] = arm.wrist_rotate.label
            yield config
