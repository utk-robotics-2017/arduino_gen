class encoder:
    def __init__(self, label, pinA, pinB):
        self.label = label
        self.pinA = pinA
        self.pinB = pinB


class encoders:
    def __init__(self):
        self.sensor_list = []

    def add(self, label, pinA, pinB):
        self.sensor_list.append(encoder(label, pinA, pinB))

    def get_include(self):
        return "#include \"Encoder.h\";"

    def get_pins(self):
        rv = ""
        for sensor in self.sensor_list:
            rv = rv + "const char %s_pinA = %d;\n" % (sensor.label, sensor.pinA)
            rv = rv + "const char %s_pinB = %d;\n" % (sensor.label, sensor.pinB)
        return rv

    def get_constructor(self):
        rv = ""
        for i in range(len(self.sensor_list)):
            rv = rv + "const char %s_index = %d;\n" % (self.sensor_list[i].label, i)
        rv = "Encoder encoders[%d] = {\n" % len(self.sensor_list)

        for sensor in self.sensor_list:
            rv = rv + "    Encoder(%s_pinA, %s_pinB),\n" % (sensor.label, sensor.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        return ""

    def get_response_block(self):
        rv = "    else if(args[0].equals(String(\"re\"))){ // read encoders\n"
        rv = rv + "        if(numArgs == 2){\n"
        rv = rv + "            int indexNum = args[1].toInt();\n"
        rv = rv + "            if(indexNum > -1 && indexNum < %d){\n" % len(self.sensor_list)
        rv = rv + "                Serial.println(encoders[indexNum].read());\n"
        rv = rv + "            } else {\n"
        rv = rv + "                Serial.println(\"Error: usage - re [id]\");\n"
        rv = rv + "            }\n"
        rv = rv + "        } else {\n"
        rv = rv + "            Serial.println(\"Error: usage - re [id]\");\n"
        rv = rv + "        }\n"
        rv = rv + "    }\n"

        rv = rv + "    else if(args[0].equals(String(\"ze\"))){ // zero encoders\n"
        rv = rv + "        if(numArgs == 2){\n"
        rv = rv + "            int indexNum = args[1].toInt();\n"
        rv = rv + "            if(indexNum > -1 && indexNum < %d){\n" % len(self.sensor_list)
        rv = rv + "                encoders[indexNum].write(0);\n"
        rv = rv + "                Serial.println(\"ok\");\n"
        rv = rv + "            } else {\n"
        rv = rv + "                Serial.println(\"Error: usage - ze [id]\");\n"
        rv = rv + "            }\n"
        rv = rv + "        } else {\n"
        rv = rv + "            Serial.println(\"Error: usage - ze [id]\");\n"
        rv = rv + "        }\n"
        rv = rv + "    }\n"
        return rv
