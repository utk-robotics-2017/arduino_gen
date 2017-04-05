from .component_list import ComponentList


class PID:
    def __init__(self, label, kp, ki, kd, min_output=None, max_output=None, reverse=False):
        self.label = label
        self.kp = float(kp)
        self.ki = float(ki)
        self.kd = float(kd)
        if min_output is not None:
            self.min_output = float(min_output)
            self.max_output = float(max_output)
        self.reverse = reverse


class PidList(ComponentList):
    TIER = 1

    def __init__(self):
        self.pid_list = []

    def add(self, json_item, device_dict, device_type):
        if 'min_output' in json_item:
            min_output = json_item['min_output']
            max_output = json_item['max_output']
        else:
            min_output = None
            max_output = None

        pid = PID(json_item['label'], json_item['kp'], json_item['ki'], json_item['kd'],
                  min_output, max_output, json_item['reverse'])
        self.pid_list.append(pid)

        return pid

    def get_includes(self):
        return '#include "PID.h"\n'

    def get_constructors(self):
        rv = ""
        length_pids = len(self.pid_list)
        for i, pid in enumerate(self.pid_list):
            rv += "const byte {0:s}_index = {1:d};\n".format(pid.label, i)
        rv += ("double lastPositions_pid[{0:d}];\ndouble Inputs_pid[{0:d}], " +
               "Setpoints_pid[{0:d}], Outputs_pid[{0:d}];\n").format(length_pids)
        rv += "PID pids[{0:d}] = {{\n".format(length_pids)
        for pid in self.pid_list:
            rv += ("\tPID(&Inputs_pid[{0:s}_index], &Outputs_pid[{0:s}_index], " +
                   "&Setpoints_pid[{0:s}_index], {1:f}, {2:f}, {3:f}, {4:s}),\n")\
                    .format(pid.label, pid.kp, pid.ki, pid.kd,
                            "REVERSE" if pid.reverse else "DIRECT")
        rv = rv[:-2] + "\n};\n"

        return rv

    def get_setup(self):
        rv = ""
        for pid in self.pid_list:
            if hasattr(pid, 'min_output'):
                rv += "\tpids[{0:s}_index].SetOutputLimits({1:f}, {2:f});\n"\
                      .format(pid.label, pid.min_output, pid.max_output)
            rv += "\tpids[{0:s}_index].SetMode(AUTOMATIC);\n".format(pid.label)
        return rv

    def get_commands(self):
        rv = "\tkGetPidConstants,\n"
        rv += "\tkGetPidConstantsResult,\n"
        rv += "\tkSetPidConstants,\n"
        rv += "\tkSetPidSetpoint,\n"
        rv += "\tkGetPidValues,\n"
        rv += "\tkGetPidValuesResult,\n"
        rv += "\tkPidOff,\n"
        return rv

    def get_command_attaches(self):
        rv = "\tcmdMessenger.attach(kGetPidConstants, getPidConstants);\n"
        rv += "\tcmdMessenger.attach(kSetPidConstants, setPidConstants);\n"
        rv += "\tcmdMessenger.attach(kSetPidSetpoint, setPidSetpoint);\n"
        rv += "\tcmdMessenger.attach(kGetPidValues, getPidValues);\n"
        rv += "\tcmdMessenger.attach(kPidOff, pidOff);\n"
        return rv

    def get_command_functions(self):
        rv = "void getPidConstants() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.pid_list))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kGetPidConstants);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kGetPidConstants);\n"
        rv += "\tcmdMessenger.sendCmdStart(kGetPidConstantsResult);\n"
        rv += "\tcmdMessenger.sendCmdBinArg(pids[indexNum].GetKp());\n"
        rv += "\tcmdMessenger.sendCmdBinArg(pids[indexNum].GetKi());\n"
        rv += "\tcmdMessenger.sendCmdBinArg(pids[indexNum].GetKd());\n"
        rv += "\tcmdMessenger.sendCmdEnd();\n"
        rv += "}\n\n"

        rv += "void setPidConstants() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.pid_list))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kSetPidConstants);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tfloat constants[3];\n"
        rv += "\tfor(int i = 0; i < 3; i++) {\n"
        rv += "\t\t\tconstants[i] = cmdMessenger.readBinArg<float>();\n"
        rv += "\t\tif(!cmdMessenger.isArgOk()){\n"
        rv += "\t\t\tcmdMessenger.sendBinCmd(kError, kSetPidConstants);\n"
        rv += "\t\t\treturn;\n"
        rv += "\t\t}\n"
        rv += "\t}\n"
        rv += "\tpids[indexNum].SetTunings(constants[0], constants[1], constants[2]);\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kSetPidConstants);\n"
        rv += "}\n\n"

        rv += "void setPidSetpoint() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.pid_list))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kSetPidSetpoint);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tfloat value = cmdMessenger.readBinArg<float>();\n"
        rv += "\tif(!cmdMessenger.isArgOk()) {\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kSetPidSetpoint);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tpids[indexNum].SetMode(AUTOMATIC);\n"
        rv += "\tSetpoints_pid[indexNum] = value;\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kSetPidSetpoint);\n"
        rv += "}\n\n"

        rv += "void getPidValues() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.pid_list))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kGetPidValues);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kGetPidValues);\n"
        rv += "\tcmdMessenger.sendCmdStart(kGetPidValuesResult);\n"
        rv += "\tcmdMessenger.sendCmdBinArg(Inputs_pid[indexNum]);\n"
        rv += "\tcmdMessenger.sendCmdBinArg(Outputs_pid[indexNum]);\n"
        rv += "\tcmdMessenger.sendCmdBinArg(Setpoints_pid[indexNum]);\n"
        rv += "\tcmdMessenger.sendCmdEnd();\n"
        rv += "}\n\n"

        rv += "void pidOff() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.pid_list))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kPidOff);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tpids[indexNum].SetMode(MANUAL);\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kPidOff);\n"
        rv += "}\n\n"

        return rv

    def get_core_values(self):
        for i, pid in enumerate(self.pid_list):
            a = {}
            a['index'] = i
            a['label'] = pid.label
            a['type'] = "PID"
            yield a
