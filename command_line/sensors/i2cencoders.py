class i2cencoder:
    def __init__(self, label, pinA, pinB, reverse, init_number):
        self.label = label
        self.pinA = pinA
        self.pinB = pinB
        self.reversed = reverse
        self.init_number = init_number


class i2cencoders:
    def __init__(self):
        self.sensor_list = []

    def add_sensor(self, label, pinA, pinB, reverse, init_number):
        self.sensor_list.append(i2cencoder(label, pinA, pinB, reverse, init_number))
        self.sensor_list.sort(key=lambda x: x.init_number, reverse=False)

    def get_sensor_name(self):
        return "i2cencoder"

    def get_include(self):
        return "I2CEncoder.h.h"

    def get_pins(self):
        rv = ""
        for sensor in self.sensor_list:
            rv = rv + "const char %s_pinA = %d;\n" % (sensor.label, sensor.pinA)
            rv = rv + "const char %s_pinB = %d;\n" % (sensor.label, sensor.pinB)
        return rv

    def get_constructor(self):
        rv = "I2CEncoder i2cencoders[%d];\n" % (len(self.sensor_list))
        for i in range(len(self.sensor_list)):
            rv = rv + "const char %s_index = %d;\n" % (self.sensor_list[i].label, i)
        for sensor in self.sensor_list:
            rv = rv + ("i2cencoders[%s_index] = new NewPing(%s_pin, %s_pin);\n") % (sensor.label, sensor.label, sensor.label)
        return rv

    

    def get_command(self):
        return "rus"

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
