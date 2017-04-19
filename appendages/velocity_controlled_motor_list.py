from appendages.component_list import ComponentList


class VelocityControlledMotor:
    def __init__(self, label, motor, encoder, vpid):
        self.label = label
        self.motor = motor
        self.encoder = encoder
        self.vpid = vpid


class VelocityControlledMotorList(ComponentList):
    TIER = 2

    def __init__(self):
        self.list_ = []

    def add(self, json_item, device_dict, device_type):
        if 'motor' not in device_dict:
            for device_level in device_type:
                if 'motor' in device_level:
                    device_dict['motor'] = device_level['motor']
                    break
        motor = device_dict['motor'].add(json_item['motor'], device_dict, device_type)

        if 'i2c_encoder' not in device_dict:
            for device_level in device_type:
                if 'i2c_encoder' in device_level:
                    device_dict['i2c_encoder'] = device_level['i2c_encoder']
                    break
        encoder = device_dict['i2c_encoder'].add(json_item['i2c_encoder'], device_dict, device_type)

        if 'vpid' not in device_dict:
            for device_level in device_type:
                if 'vpid' in device_level:
                    device_dict['vpid'] = device_level['vpid']
                    break
        vpid = device_dict['vpid'].add(json_item['vpid'], device_dict, device_type)

        vcm = VelocityControlledMotor(json_item['label'], motor, encoder, vpid)
        self.list_.append(vcm)
        self.list_.sort(key=lambda x: x.label, reverse=False)
        return vcm

    def get_includes(self):
        return '#include "VelocityControlledMotor.h"\n'

    def get_constructors(self):
        rv = ""
        for i, vcm in enumerate(self.list_):
            rv += "const byte {0:s}_index = {1:d};\n".format(vcm.label, i)
        rv += "VelocityControlledMotor vcms[{0:d}] = {{\n".format(len(self.list_))
        for vcm in self.list_:
            rv += ("\tVelocityControlledMotor(motors[{0:s}_index], i2c_encoders[{1:s}_index], " +
                   "vpids[{2:s}_index], &Inputs_vpid[{2:s}_index], " +
                   "&Outputs_vpid[{2:s}_index], &Setpoints_vpid[{2:s}_index]),\n")\
                .format(vcm.motor.label, vcm.encoder.label, vcm.vpid.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_loop_functions(self):
        return "\tfor(int i = 0; i < {0:d}; i++) {{\n\t\t\tvcms[i].runVPID();\n\t\t}}\n".format(
            len(self.list_))

    def get_commands(self):
        rv = "\tkSetVCMVoltage,\n"
        rv += "\tkSetVCMVelocity,\n"
        rv += "\tkStopVCM,\n"
        rv += "\tkGetVCMVelocity,\n"
        rv += "\tkGetVCMVelocityResult,\n"
        rv += "\tkGetVCMPosition,\n"
        rv += "\tkGetVCMPositionResult,\n"
        return rv

    def get_command_attaches(self):
        rv = "\tcmdMessenger.attach(kSetVCMVoltage, setVCMVoltage);\n"
        rv += "\tcmdMessenger.attach(kSetVCMVelocity, setVCMVelocity);\n"
        rv += "\tcmdMessenger.attach(kStopVCM, stopVCM);\n"
        rv += "\tcmdMessenger.attach(kGetVCMVelocity, getVCMVelocity);\n"
        rv += "\tcmdMessenger.attach(kGetVCMPosition, getVCMPosition);\n"
        return rv

    def get_command_functions(self):
        rv = "void setVCMVoltage() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n"\
            .format(len(self.list_))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kSetVCMVoltage);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tint value = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(cmdMessenger.isArgOk() && value > -1024 && value < 1024) {\n"
        rv += "\t\tvcms[indexNum].setValue(value);\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kAcknowledge, kSetVCMVoltage);\n"
        rv += "\t} else {\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kSetVCMVoltage);\n"
        rv += "\t}\n"
        rv += "}\n\n"

        rv += "void setVCMVelocity() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n"\
            .format(len(self.list_))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kSetVCMVelocity);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tfloat value = cmdMessenger.readBinArg<float>();\n"
        rv += "\tif(!cmdMessenger.isArgOk()){\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kSetVCMVelocity);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tvcms[indexNum].setVelocity(value);\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kSetVCMVelocity);\n"
        rv += "}\n\n"

        rv += "void stopVCM() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n"\
            .format(len(self.list_))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kStopVCM);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tvcms[indexNum].stop();\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kStopVCM);\n"
        rv += "}\n\n"

        rv += "void getVCMVelocity() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n"\
            .format(len(self.list_))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kGetVCMVelocity);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kSetVCMVelocity);\n"
        rv += "\tcmdMessenger.sendBinCmd(kGetVCMVelocityResult, vcms[indexNum].getVelocity());\n"
        rv += "}\n\n"

        rv += "void getVCMPosition() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n"\
            .format(len(self.list_))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kGetVCMPosition);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kGetVCMPosition);\n"
        rv += "\tcmdMessenger.sendBinCmd(kGetVCMPositionResult, vcms[indexNum].getPosition());\n"
        rv += "}\n\n"

        return rv

    def get_core_values(self):
        for i, vcm in enumerate(self.list_):
            config = {}
            config['index'] = i
            config['label'] = vcm.label
            config['type'] = "Velocity Controlled Motor"
            config['motor'] = vcm.motor.label
            config['i2c_encoder'] = vcm.encoder.label
            config['vpid'] = vcm.vpid.label
            yield config
