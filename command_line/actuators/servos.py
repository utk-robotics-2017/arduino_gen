class servo:
    def __init__(self, label, pin):
        self.label = label
        self.pin = pin


class servos:
    def __init__(self):
        self.actuator_list = []

    def add_actuator(self, label, pin):
        self.actuator_list.append(servo(label, pin))

    def get_sensor_name(self):
        return "servo"

    def get_include(self):
        return "#include \"Servo.h\";"

    def get_pins(self):
        rv = ""
        for actuator in self.actuator_list:
            rv = rv + "const char %s_pin = %d;\n" % (actuator.label, actuator.pin)
        return rv

    def get_constructor(self):
        rv = ""
        for i in range(len(self.actuator_list)):
            rv = rv + "const char %s_index = %d;\n" % (self.actuator_list[i].label, i)
        rv = rv + ("Servo servos[%d];\n") % (len(self.actuator_list))
        return rv

    def get_setup(self):
        rv = ""
        for actuator in self.actuator_list:
            rv = rv + "    servos[%s_index].attach(%s_pin);\n" % (actuator.label, actuator.label)
        rv = rv + "\n"
        return rv

    def get_command(self):
        return "ss"

    def get_response_block(self):
        rv = "    else if(args[0].equals(String(\"ss\"))){ // set servo\n"
        rv = rv + "        if(numArgs == 3){\n"
        rv = rv + "            int indexNum = args[1].toInt();\n"
        rv = rv + "            if(indexNum > -1 && indexNum < %d){\n" % len(self.actuator_list)
        rv = rv + "                int value = args[2].toInt();\n"
        rv = rv + "                servos[indexNum].write(value);\n"
        rv = rv + "                Serial.println(\"ok\");\n"
        rv = rv + "            } else {\n"
        rv = rv + "                Serial.println(\"Error: usage - ss [id] [value]\");\n"
        rv = rv + "            }\n"
        rv = rv + "        } else {\n"
        rv = rv + "            Serial.println(\"Error: usage - ss [id] [value]\");\n"
        rv = rv + "        }\n"
        rv = rv + "    }\n"
        return rv
