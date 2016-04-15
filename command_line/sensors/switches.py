class switch:
    def __init__(self, label, pin, pullup):
        self.label = label
        self.pin = pin
        self.pullup = pullup


class switches:
    def __init__(self):
        self.sensor_list = []

    def add(self, label, pin, pullup):
        self.sensor_list.append(switch(label, pin, pullup))

    def get_include(self):
        return ""

    def get_pins(self):
        rv = ""
        for sensor in self.sensor_list:
            rv = rv + "const char %s_pin = %d;\n" % (sensor.label, sensor.pin)
        return rv

    def get_constructor(self):
        rv = ""
        for i in range(len(self.sensor_list)):
            rv = rv + "const char %s_index = %d;\n" % (self.sensor_list[i].label, i)
        rv = rv + "char switches[%d] = {\n" % (len(self.sensor_list))
        for sensor in self.sensor_list:
            rv = rv + ("    %s_pin,\n") % (sensor.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        rv = ""
        for sensor in self.sensor_list:
            if sensor.pullup:
                rv = rv + "    pinMode(%s_pin, INPUT_PULLUP);\n" % sensor.label
            else:
                rv = rv + "    pinMode(%s_pin, INPUT);\n" % sensor.label
        rv = rv + "\n"
        return rv

    def get_response_block(self):
        rv = "    else if(args[0].equals(String(\"rs\"))){ // read switches\n"
        rv = rv + "        if(numArgs == 2){\n"
        rv = rv + "            int indexNum = args[1].toInt();\n"
        rv = rv + "            if(indexNum > -1 && indexNum < %d){\n" % len(self.sensor_list)
        rv = rv + "                Serial.println(digitalRead(switches[indexNum]));\n"
        rv = rv + "            } else {\n"
        rv = rv + "                Serial.println(\"Error: usage - rs [id]\");\n"
        rv = rv + "            }\n"
        rv = rv + "        } else {\n"
        rv = rv + "            Serial.println(\"Error: usage - rs [id]\");\n"
        rv = rv + "        }\n"
        rv = rv + "    }\n"
        return rv
