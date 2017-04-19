from appendages.component_list import ComponentList


class PositionControlledMotor:
    def __init__(self, label, motor, encoder, pid):
        self.label = label
        self.motor = motor
        self.encoder = encoder
        self.pid = pid


class PositionControlledMotorList(ComponentList):
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

        if 'pid' not in device_dict:
            for device_level in device_type:
                if 'pid' in device_level:
                    device_dict['pid'] = device_level['pid']
                    break
        pid = device_dict['pid'].add(json_item['pid'], device_dict, device_type)

        pcm = PositionControlledMotor(json_item['label'], motor, encoder, pid)
        self.list_.append(pcm)
        self.list_.sort(key=lambda x: x.label, reverse=False)
        return pcm

    def get_includes(self):
        return '#include "PositionControlledMotor.h"\n'

    def get_constructors(self):
        rv = ""
        for i, pcm in enumerate(self.list_):
            rv += "const byte {0:s}_index = {1:d};\n".format(pcm.label, i)
        rv += "PositionControlledMotor pcms[{0:d}] = {{\n".format(len(self.list_))
        for pcm in self.list_:
            rv += ("\tPositionControlledMotor(motors[{0:s}_index], i2c_encoders[{1:s}_index], " +
                   "pids[{2:s}_index], &Inputs_pid[{2:s}_index], " +
                   "&Outputs_pid[{2:s}_index], &Setpoints_pid[{2:s}_index]),\n")\
                .format(pcm.motor.label, pcm.encoder.label, pcm.pid.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_loop_functions(self):
        return "\tfor(int i = 0; i < {0:d}; i++) {{\n\t\t\tpcms[i].runPID();\n\t\t}}\n".format(
            len(self.list_))

    def get_commands(self):
        rv = "\tkSetPCMVoltage,\n"
        rv += "\tkStopPCM,\n"
        rv += "\tkGetPCMPosition,\n"
        rv += "\tkGetPCMPositionResult,\n"
        rv += "\tkSetPCMPosition,\n"
        return rv

    def get_command_attaches(self):
        rv = "\tcmdMessenger.attach(kSetPCMVoltage, setPCMVoltage);\n"
        rv += "\tcmdMessenger.attach(kStopPCM, stopPCM);\n"
        rv += "\tcmdMessenger.attach(kGetPCMPosition, getPCMPosition);\n"
        rv += "\tcmdMessenger.attach(kSetPCMPosition, setPCMPosition);\n"
        return rv

    def get_command_functions(self):
        rv = "void setPCMVoltage() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n"\
            .format(len(self.list_))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kSetPCMVoltage);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tint value = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(cmdMessenger.isArgOk() && value > -1024 && value < 1024) {\n"
        rv += "\t\tpcms[indexNum].setValue(value);\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kAcknowledge, kSetPCMVoltage);\n"
        rv += "\t} else {\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kSetPCMVoltage);\n"
        rv += "\t}\n"
        rv += "}\n\n"

        rv += "void stopPCM() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n"\
            .format(len(self.list_))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kStopPCM);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tpcms[indexNum].stop();\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kStopPCM);\n"
        rv += "}\n\n"

        rv += "void getPCMPosition() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n"\
            .format(len(self.list_))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kGetPCMPosition);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kGetPCMPosition);\n"
        rv += "\tcmdMessenger.sendBinCmd(kGetPCMPositionResult, pcms[indexNum].getPosition());\n"
        rv += "}\n\n"

        rv += "void setPCMPosition() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n"\
            .format(len(self.list_))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kSetPCMPosition);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tfloat value = cmdMessenger.readBinArg<float>();\n"
        rv += "\tif(!cmdMessenger.isArgOk()){\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kSetPCMPosition);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tpcms[indexNum].setPosition(value);\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kSetPCMPosition);\n"
        rv += "}\n\n"

        return rv

    def get_core_values(self):
        for i, pcm in enumerate(self.list_):
            config = {}
            config['index'] = i
            config['label'] = pcm.label
            config['type'] = "Position Controlled Motor"
            config['motor'] = pcm.motor.label
            config['encoder'] = pcm.encoder.label
            config['pid'] = pcm.pid.label
            yield config
