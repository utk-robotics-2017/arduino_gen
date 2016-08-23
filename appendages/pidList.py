class pid:
    def __init__(self, label, kp, ki, kd, minOutput=None, maxOutput=None, reverse=False):
        self.label = label
        self.kp = float(kp)
        self.ki = float(ki)
        self.kd = float(kd)
        if not minOutput is None:
            self.minOutput = float(minOutput)
            self.maxOutput = float(maxOutput)
        self.reverse = reverse


class pidList:
    def __init__(self):
        self.pids = dict()
        self.vpids = dict()

    def add(self, json_item):
        if 'minOutput' in json_item:
            minOutput = json_item['minOutput']
            maxOutput = json_item['maxOutput']
        else:
            minOutput = None
            maxOutput = None

        if json_item['vpid']:
            self.vpids[json_item['label']] = pid(json_item['label'], json_item['kp'], json_item['ki'], json_item['kd'], minOutput, maxOutput, json_item['reverse'])
        else:
            self.pids[json_item['label']] = pid(json_item['label'], json_item['kp'], json_item['ki'], json_item['kd'], minOutput, maxOutput, json_item['reverse'])

    def get(self, label):
        if label in self.vpids.keys():
            return self.vpids[label]
        else:
            return self.pids[label]

    def get_include(self):
        return "#include \"PID.h\"\n#include \"vPID.h\""

    def get_include_files(self):
        return ['PID.h', 'PID.cpp', 'vPID.h', 'vPID.cpp']

    def get_pins(self):
        return ""

    def get_constructor(self):
        rv = ""
        length_vpids = len(self.vpids)
        if length_vpids > 0:
            for i, label in zip(range(length_vpids), self.vpids.keys()):
                rv = rv + "const char %s_index = %d;\n" % (label, i)
            rv += "double lastPositions_vpid[%d];\ndouble Inputs_vpid[%d], Setpoints_vpid[%d], Outputs_vpid[%d];\n" % (length_vpids, length_vpids, length_vpids, length_vpids)
            rv += "vPID vpids[%d] = {\n" % (length_vpids)
            for vpid in self.vpids.values():
                rv += "    vPID(&Inputs_vpid[%s_index], &Outputs_vpid[%s_index], &Setpoints_vpid[%s_index], %f, %f, %f, %s),\n" % (vpid.label, vpid.label, vpid.label, vpid.kp, vpid.ki, vpid.kd, "REVERSE" if vpid.reverse else "DIRECT")
            rv = rv[:-2] + "\n};\n"

        length_pids = len(self.pids)
        if length_pids > 0:
            for i, label in zip(range(len(self.pids)), self.pids.keys()):
                rv = rv + "const char %s_index = %d;\n" % (label, i)
            rv += "double lastPositions_pid[%d];\ndouble Inputs_pid[%d], Setpoints_pid[%d], Outputs_pid[%d];\n" % (length_vpids, length_vpids, length_vpids, length_vpids)
            rv += "PID pids[%d] = {\n" % (length_pids)
            for pid in self.pids.values():
                rv += "    PID(&Inputs_pid[%s_index], &Outputs_pid[%s_index], &Setpoints_pid[%s_index], %f, %f, %f, %s),\n" % (vpid.label, vpid.label, vpid.label, vpid.kp, vpid.ki, vpid.kd, "REVERSE" if vpid.reverse else "DIRECT")
            rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        rv = ""
        for vpid in self.vpids.values():
            if hasattr(vpid, 'minOutput'):
                rv += "    vpid.SetOutputLimits(%f, %f)\n" % (vpid.minOutput, vpid.maxOutput)
        return rv

    def get_loop_functions(self):
        return ""

    def get_response_block(self):
        length_vpids = len(self.vpids)
        length_pids = len(self.pids)
        rv = ""
        if length_pids > 0:
            rv += '''    else if (args[0].equals(String("pc"))) { // Modify the pid constants
    if (numArgs == 5) {
      int indexNum = args[1].toInt();
      if (indexNum > -1 && indexNum < %d) {
        pids[indexNum].SetTunings(toDouble(args[2]), toDouble(args[3]), toDouble(args[4]));
        Serial.println("ok");
      } else {
        Serial.println(F("error: usage - 'pc [index] [kp] [ki] [kd]'"));
      }
    } else {
      Serial.println(F("error: usage - 'pc [index] [kp] [ki] [kd]'"));
    }
  }
  else if (args[0].equals(String("ps"))) { // Set the setpoint for a specific PID
    if (numArgs == 3) {
      int indexNum = args[1].toInt();
      if (indexNum > -1 && indexNum < %d) {
        pids[indexNum].SetMode(AUTOMATIC);
        Setpoints_pid[indexNum] = toDouble(args[2]);
        Serial.println(F("ok"));
      } else {
        Serial.println(F("error: usage - 'ps [index] [setpoint]'"));
      }
    } else {
      Serial.println(F("error: usage - 'ps [index] [setpoint]'"));
    }
  }
  else if (args[0].equals(String("poff"))) { // Turn off the PID
    if (numArgs == 2) {
      int indexNum = args[1].toInt();
      if (indexNum > -1 && indexNum < %d) {
        pids[indexNum].SetMode(MANUAL);
        Serial.println(F("ok"));
      } else {
        Serial.println(F("error: usage - 'poff [index]'"));
      }
    } else {
      Serial.println(F("error: usage - 'poff [index]'"));
    }
  }
  else if (args[0].equals(String("pd"))) { // Display Inputs, Setpoints, and Outputs
    if (numArgs == 2) {
      int indexNum = args[1].toInt();
      if (indexNum > -1 && indexNum < %d) {
        String ret = "";
        ret += Inputs_pid[indexNum];
        ret += " ";
        ret += Setpoints_pid[indexNum];
        ret += " ";
        ret += Outputs_pid[indexNum];
        Serial.println(ret);
        } else {
        Serial.println(F("error: usage - 'pd [index]'"));
      }
    } else {
      Serial.println(F("error: usage - 'pd [index]'"));
    }
  }
''' % (length_pids, length_pids, length_pids, length_pids)

        if length_vpids > 0:
            rv += '''    else if (args[0].equals(String("vpc"))) { // Modify the velocity pid constants
    if (numArgs == 5) {
      int indexNum = args[1].toInt();
      if (indexNum > -1 && indexNum < %d) {
        vpids[indexNum].SetTunings(toDouble(args[2]), toDouble(args[3]), toDouble(args[4]));
        Serial.println("ok");
      } else {
        Serial.println(F("error: usage - 'vpc [index] [kp] [ki] [kd]'"));
      }
    } else {
      Serial.println(F("error: usage - 'vpc [index] [kp] [ki] [kd]'"));
    }
  }
  else if (args[0].equals(String("vps"))) { // Set the setpoint for a specific PID
    if (numArgs == 3) {
      int indexNum = args[1].toInt();
      if (indexNum > -1 && indexNum < %d) {
        vpids[indexNum].SetMode(AUTOMATIC);
        Setpoints_vpid[indexNum] = toDouble(args[2]);
        Serial.println(F("ok"));
      } else {
        Serial.println(F("error: usage - 'vps [index] [setpoint]'"));
      }
    } else {
      Serial.println(F("error: usage - 'vps [index] [setpoint]'"));
    }
  }
  else if (args[0].equals(String("vpoff"))) { // Turn off the PID
    if (numArgs == 2) {
      int indexNum = args[1].toInt();
      if (indexNum > -1 && indexNum < %d) {
        vpids[indexNum].SetMode(MANUAL);
        Serial.println(F("ok"));
      } else {
        Serial.println(F("error: usage - 'vpoff [index]'"));
      }
    } else {
      Serial.println(F("error: usage - 'vpoff [index]'"));
    }
  }
  else if (args[0].equals(String("vpd"))) { // Display Inputs, Setpoints, and Outputs
    if (numArgs == 2) {
      int indexNum = args[1].toInt();
      if (indexNum > -1 && indexNum < %d) {
        String ret = "";
        ret += Inputs_vpid[indexNum];
        ret += " ";
        ret += Setpoints_vpid[indexNum];
        ret += " ";
        ret += Outputs_vpid[indexNum];
        Serial.println(ret);
        } else {
        Serial.println(F("error: usage - 'vpd [index]'"));
      }
    } else {
      Serial.println(F("error: usage - 'vpd [index]'"));
    }
  }
''' % (length_vpids, length_vpids, length_vpids, length_vpids)
        return rv

    # extra functions for loop are written by the systems using the pid
    def get_extra_functions(self):
        return ""
