from appendages.i2c_encoder_list import I2CEncoder
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
        motor = device_dict['motor'].add(json_item['motor'])

        if 'i2cencoder' in json_item:
            if 'i2cencoder' not in device_dict:
                for device_level in device_type:
                    if 'i2cencoder' in device_level:
                        device_dict['i2cencoder'] = device_level['i2cencoder']
                        break
            encoder = device_dict['i2cencoder'].add(json_item['i2cencoder'])
        else:
            if 'encoder' not in device_dict:
                for device_level in device_type:
                    if 'encoder' in device_level:
                        device_dict['encoder'] = device_level['encoder']
                        break
            encoder = device_dict['encoder'].add(json_item['encoder'])
        if 'pid' not in device_dict:
            for device_level in device_type:
                if 'pid' in device_level:
                    device_dict['pid'] = device_level['pid']
                    break
        vpid = device_dict.add(json_item['pid'])
        vcm = VelocityControlledMotor(json_item['label'], motor, encoder, vpid)
        self.list_.append(vcm)
        self.list_.sort(key=lambda x: x.label, reverse=False)
        return vcm

    def get_includes(self):
        return '#include "VelocityControlledMotor.h"\n'

    def get_constructor(self):
        rv = ""
        for i, vcm in enumerate(self.list_):
            rv += "const char {0:s}_index = {1:d};\n".format(vcm.label, i)
        rv += "VelocityControlledMotor vcms[{0:d}] = {{\n".format(len(self.list_))
        for vcm in self.list_:
            if isinstance(vcm.encoder, I2CEncoder):
                rv += ("\tVelocityControlledMotor(motors[{0:s}_index], i2cencoders[{1:s}_index], " +
                       "vpids[{2:s}_index], &Inputs_vpid[{2:s}_index], " +
                       "&Setpoints_vpid[{2:s}_index], &Outputs_vpid[{2:s}_index]),\n")\
                    .format(vcm.motor.label, vcm.encoder.label, vcm.vpid.label)
            else:
                rv += ("\tVelocityControlledMotor(motors[{0:s}_index], encoders[{1:s}_index], " +
                       "vpids[{2:s}_index], &Inputs_vpid[{2:s}_index], " +
                       "&Setpoints_vpid[{2:s}_index], &Outputs_vpid[{2:s}_index]),\n")\
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
            config['encoder'] = vcm.encoder.label
            config['vpid'] = vcm.vpid.label
            yield config
