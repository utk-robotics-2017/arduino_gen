class Pid:
    def __init__(self, label, kp, ki, kd, minOutput=None, maxOutput=None, reverse=False):
        self.label = label
        self.kp = float(kp)
        self.ki = float(ki)
        self.kd = float(kd)
        if minOutput is not None:
            self.minOutput = float(minOutput)
            self.maxOutput = float(maxOutput)
        self.reverse = reverse


class pidList:
    def __init__(self):
        self.tier = 1
        self.pidDict = {}
        self.pidList = []
        self.vpidDict = {}
        self.vpidList = []

    def add(self, json_item):
        if 'minOutput' in json_item:
            minOutput = json_item['minOutput']
            maxOutput = json_item['maxOutput']
        else:
            minOutput = None
            maxOutput = None

        if not json_item['vpid']:
            pid = Pid(json_item['label'], json_item['kp'], json_item['ki'], json_item['kd'],
                      minOutput, maxOutput, json_item['reverse'])
            self.pidDict[pid.label] = pid
            self.pidList.append(pid)
            self.pidList.sort(key=lambda x: x.label, reverse=False)
        else:
            pid = Pid(json_item['label'], json_item['kp'], json_item['ki'], json_item['kd'],
                      minOutput, maxOutput, json_item['reverse'])
            self.vpidDict[pid.label] = pid
            self.vpidList.append(pid)
            self.vpidList.sort(key=lambda x: x.label, reverse=False)

    def get(self, label):
        if label in list(self.vpidDict.keys()):
            return self.vpidDict[label]
        else:
            return self.pidDict[label]

    def get_include(self):
        return "#include \"PID.h\"\n#include \"vPID.h\""

    def get_pins(self):
        return ""

    def get_constructor(self):
        rv = ""
        length_vpids = len(self.vpidList)
        if length_vpids > 0:
            for i, vpid in enumerate(self.vpidList):
                rv += "const char {0:s}_index = {1:d};\n".format(vpid.label, i)
            rv += ("double lastPositions_vpid[{0:d}];\ndouble Inputs_vpid[{0:d}], " +
                   "Setpoints_vpid[{0:d}], Outputs_vpid[{0:d}];\n").format(length_vpids)
            rv += "vPID vpids[{0:d}] = {{\n".format(length_vpids)
            for vpid in self.vpidList:
                rv += ("\tvPID(&Inputs_vpid[{0:s}_index], &Outputs_vpid[{0:s}_index], " +
                       "&Setpoints_vpid[{0:s}_index], {1:f}, {2:f}, {3:f}, {4:s}),\n")\
                        .format(vpid.label, vpid.kp, vpid.ki, vpid.kd,
                                "REVERSE" if vpid.reverse else "DIRECT")
            rv = rv[:-2] + "\n};\n"

        length_pids = len(self.pidList)
        if length_pids > 0:
            for i, pid in enumerate(self.pidList):
                rv += "const char {0:s}_index = {1:d};\n".format(pid.label, i)
            rv += ("double lastPositions_pid[{0:d}];\ndouble Inputs_pid[{0:d}], " +
                   "Setpoints_pid[{0:d}], Outputs_pid[{0:d}];\n").format(length_pids)
            rv += "PID pids[{0:d}] = \{\n".format(length_pids)
            for pid in self.pidList:
                rv += ("\tPID(&Inputs_pid[{0:s}_index], &Outputs_pid[{0:s}_index], " +
                       "&Setpoints_pid[{0:s}_index], {1:f}, {2:f}, {3:f}, {4:s}),\n")\
                        .format(pid.label, pid.kp, pid.ki, pid.kd,
                                "REVERSE" if pid.reverse else "DIRECT")
            rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        rv = ""
        for vpid in self.vpidList:
            if hasattr(vpid, 'minOutput'):
                rv += ("\tvpids[{0:s}_index].SetOutputLimits({1:f}, {2:f});\n")\
                        .format(vpid.label, vpid.minOutput, vpid.maxOutput)
        for pid in self.pidList:
            if hasattr(pid, 'minOutput'):
                rv += ("\tpids[{0:s}_index].SetOutputLimits({1:f}, {2:f});\n")\
                        .format(pid.label, pid.minOutput, pid.maxOutput)
        return rv

    def get_loop_functions(self):
        return ""

    def get_response_block(self):
        length_vpids = len(self.vpidList)
        length_pids = len(self.pidList)
        rv = ""
        if length_pids > 0:
            rv += '''    else if (args[0].equals(String("pc"))) {{ // Modify the pid constants
    if (numArgs == 5) {{
      int indexNum = args[1].toInt();
      if (indexNum > -1 && indexNum < {0:d}) {{
        pids[indexNum].SetTunings(toDouble(args[2]), toDouble(args[3]), toDouble(args[4]));
        Serial.println("ok");
      }} else {{
        Serial.println(F("error: usage - 'pc [index] [kp] [ki] [kd]'"));
      }}
    }} else {{
      Serial.println(F("error: usage - 'pc [index] [kp] [ki] [kd]'"));
    }}
  }}
  else if (args[0].equals(String("ps"))) {{ // Set the setpoint for a specific PID
    if (numArgs == 3) {{
      int indexNum = args[1].toInt();
      if (indexNum > -1 && indexNum < {0:d}) {{
        pids[indexNum].SetMode(AUTOMATIC);
        Setpoints_pid[indexNum] = toDouble(args[2]);
        Serial.println(F("ok"));
      }} else {{
        Serial.println(F("error: usage - 'ps [index] [setpoint]'"));
      }}
    }} else {{
      Serial.println(F("error: usage - 'ps [index] [setpoint]'"));
    }}
  }}
  else if (args[0].equals(String("poff"))) {{ // Turn off the PID
    if (numArgs == 2) {{
      int indexNum = args[1].toInt();
      if (indexNum > -1 && indexNum < {0:d}) {{
        pids[indexNum].SetMode(MANUAL);
        Serial.println(F("ok"));
      }} else {{
        Serial.println(F("error: usage - 'poff [index]'"));
      }}
    }} else {{
      Serial.println(F("error: usage - 'poff [index]'"));
    }}
  }}
  else if (args[0].equals(String("pd"))) {{ // Display Inputs, Setpoints, and Outputs
    if (numArgs == 2) {{
      int indexNum = args[1].toInt();
      if (indexNum > -1 && indexNum < {0:d}) {{
        String ret = "";
        char dts[256];
        dtostrf(Inputs_pid[indexNum], 0, 6, dts);
        ret += dts;
        ret += " ";
        dtostrf(Setpoints_pid[indexNUm], 0, 6, dts);
        ret += dts;
        ret += " ";
        dtostrf(Outputs_pid[indexNum], 0, 6, dts);
        ret += dts;
        Serial.println(ret);
        }} else {{
        Serial.println(F("error: usage - 'pd [index]'"));
      }}
    }} else {{
      Serial.println(F("error: usage - 'pd [index]'"));
    }}
    }}
'''.format(length_pids)

        if length_vpids > 0:
            rv += '''    else if (args[0].equals(String("vpc"))) {{ // Modify the velocity pid constants
    if (numArgs == 5) {{
      int indexNum = args[1].toInt();
      if (indexNum > -1 && indexNum < {0:d}) {{
        vpids[indexNum].SetTunings(toDouble(args[2]), toDouble(args[3]), toDouble(args[4]));
        Serial.println("ok");
      }} else {{
        Serial.println(F("error: usage - 'vpc [index] [kp] [ki] [kd]'"));
      }}
    }} else {{
      Serial.println(F("error: usage - 'vpc [index] [kp] [ki] [kd]'"));
    }}
  }}
  else if (args[0].equals(String("vps"))) {{ // Set the setpoint for a specific PID
    if (numArgs == 3) {{
      int indexNum = args[1].toInt();
      if (indexNum > -1 && indexNum < {0:d}) {{
        vpids[indexNum].SetMode(AUTOMATIC);
        Setpoints_vpid[indexNum] = toDouble(args[2]);
        Serial.println(F("ok"));
      }} else {{
        Serial.println(F("error: usage - 'vps [index] [setpoint]'"));
      }}
    }} else {{
      Serial.println(F("error: usage - 'vps [index] [setpoint]'"));
    }}
  }}
  else if (args[0].equals(String("vpoff"))) {{ // Turn off the PID
    if (numArgs == 2) {{
      int indexNum = args[1].toInt();
      if (indexNum > -1 && indexNum < {0:d}) {{
        vpids[indexNum].SetMode(MANUAL);
        Serial.println(F("ok"));
      }} else {{
        Serial.println(F("error: usage - 'vpoff [index]'"));
      }}
    }} else {{
      Serial.println(F("error: usage - 'vpoff [index]'"));
    }}
  }}
  else if (args[0].equals(String("vpd"))) {{ // Display Inputs, Setpoints, and Outputs
    if (numArgs == 2) {{
      int indexNum = args[1].toInt();
      if (indexNum > -1 && indexNum < {0:d}) {{
        String ret = "";
        char dts[256];
        dtostrf(Inputs_vpid[indexNum], 0, 6, dts);
        ret += dts;
        ret += " ";
        dtostrf(Setpoints_vpid[indexNum], 0, 6, dts);
        ret += dts;
        ret += " ";
        dtostrf(Outputs_vpid[indexNum], 0, 6, dts);
        ret += dts;
        Serial.println(ret);
      }} else {{
        Serial.println(F("error: usage - 'vpd [index]'"));
      }}
    }} else {{
      Serial.println(F("error: usage - 'vpd [index]'"));
    }}
}}
'''.format(length_vpids)
        return rv

    # extra functions for loop are written by the systems using the pid
    def get_extra_functions(self):
        return ""

    def get_indices(self):
        for i, vpid in enumerate(self.vpidList):
            yield i, vpid
        for i, pid in enumerate(self.pidList):
            yield i, pid
