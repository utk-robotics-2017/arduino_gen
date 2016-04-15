class ultrasonic:
    def __init__(self, label, pin):
        self.label = label
        self.pin = pin


class ultrasonics:

    def __init__(self):
        self.sensor_list = []

    def add(self, label, pin):
        self.sensor_list.append(ultrasonic(label, pin))

    def get_include(self):
        return "#include \"NewPing.h\";"

    def get_pins(self):
        rv = ""
        for sensor in self.sensor_list:
            rv = rv + "const char %s_pin = %d;\n" % (sensor.label, sensor.pin)
        return rv

    def get_constructor(self):
        rv = ""
        for i in range(len(self.sensor_list)):
            rv = rv + "const char %s_index = %d;\n" % (self.sensor_list[i].label, i)
        rv = "NewPing ultrasonics[%d] = {\n" % len(self.sensor_list)

        for sensor in self.sensor_list:
            rv = rv + "    NewPing(%s_pin, %s_pin),\n" % (sensor.label, sensor.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        return ""

    def get_response_block(self):
        rv = "    else if(args[0].equals(String(\"rus\"))){ // read ultrasonics\n"
        rv = rv + "        if(numArgs == 2){\n"
        rv = rv + "            int indexNum = args[1].toInt();\n"
        rv = rv + "            if(indexNum > -1 && indexNum < %d){\n" % len(self.sensor_list)
        rv = rv + "                unsigned int response = ultrasonics[indexNum].ping();\n"
        rv = rv + "                Serial.println(response);\n"
        rv = rv + "            } else {\n"
        rv = rv + "                Serial.println(\"Error: usage - rus [id]\");\n"
        rv = rv + "            }\n"
        rv = rv + "        } else {\n"
        rv = rv + "            Serial.println(\"Error: usage - rus [id]\");\n"
        rv = rv + "        }\n"
        rv = rv + "    }\n"
        return rv
