class i2cencoder:
    def __init__(self, label, pinA, pinB, reverse, init_number):
        self.label = label
        self.pinA = pinA
        self.pinB = pinB
        self.reverse = reverse
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
        return "I2CEncoder.h"

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
        return rv

    def get_setup(self):
        rv = "    Wire.begin();\n"
        for sensor in self.sensor_list:
            rv = rv + "    i2cencoders[%s_index].init(MOTOR_393_TORQUE_ROTATIONS, MOTOR_393_TIME_DELTA);\n" % sensor.label
        for sensor in self.sensor_list:
            if sensor.reverse:
                rv = rv + "    i2cencoders[%s_index].setReversed(true);\n" % sensor.label
        for sensor in self.sensor_list:
            rv = rv + "    i2cencoders[%s_index].zero();\n" % sensor.label
        rv = rv + "\n"
        return rv

    def get_command(self):
        return "rus"

    def get_response_block(self):
        rv = "    else if(args[0].equals(String(\"ep\"))){ // encoder position (in rotations)\n"
        rv = rv + "        if(numArgs == 2){\n"
        rv = rv + "            int indexNum = args[1].toInt();\n"
        rv = rv + "            if(indexNum > -1 && indexNum < %d){\n" % len(self.sensor_list)
        rv = rv + "                char dts[256];\n"
        rv = rv + "                dtostrf(i2cencoders[indexNum].getPosition(), 0, 6, dts);\n"
        rv = rv + "                Serial.println(dts);\n"
        rv = rv + "            } else {\n"
        rv = rv + "                Serial.println(\"Error: usage - ep [id]\");\n"
        rv = rv + "            }\n"
        rv = rv + "        } else {\n"
        rv = rv + "            Serial.println(\"Error: usage - ep [id]\");\n"
        rv = rv + "        }\n"
        rv = rv + "    }\n"

        rv = rv + "    else if(args[0].equals(String(\"erp\"))){ // i2c encoder raw position (in ticks)\n"
        rv = rv + "        if(numArgs == 2){\n"
        rv = rv + "            int indexNum = args[1].toInt();\n"
        rv = rv + "            if(indexNum > -1 && indexNum < %d){\n" % len(self.sensor_list)
        rv = rv + "                char dts[256];\n"
        rv = rv + "                dtostrf(i2cencoders[indexNum].getRawPosition(), 0, 6, dts);\n"
        rv = rv + "                Serial.println(dts);\n"
        rv = rv + "            } else {\n"
        rv = rv + "                Serial.println(\"Error: usage - erp [id]\");\n"
        rv = rv + "            }\n"
        rv = rv + "        } else {\n"
        rv = rv + "            Serial.println(\"Error: usage - erp [id]\");\n"
        rv = rv + "        }\n"
        rv = rv + "    }\n"

        rv = rv + "    else if(args[0].equals(String(\"es\"))){ // i2c encoder speed (in revolutions per minute)\n"
        rv = rv + "        if(numArgs == 2){\n"
        rv = rv + "            int indexNum = args[1].toInt();\n"
        rv = rv + "            if(indexNum > -1 && indexNum < %d){\n" % len(self.sensor_list)
        rv = rv + "                char dts[256];\n"
        rv = rv + "                dtostrf(i2cencoders[indexNum].getSpeed(), 0, 6, dts);\n"
        rv = rv + "                Serial.println(dts);\n"
        rv = rv + "            } else {\n"
        rv = rv + "                Serial.println(\"Error: usage - es [id]\");\n"
        rv = rv + "            }\n"
        rv = rv + "        } else {\n"
        rv = rv + "            Serial.println(\"Error: usage - es [id]\");\n"
        rv = rv + "        }\n"
        rv = rv + "    }\n"

        rv = rv + "    else if(args[0].equals(String(\"ez\"))){ // i2c encoder zero\n"
        rv = rv + "        if(numArgs == 2){\n"
        rv = rv + "            int indexNum = args[1].toInt();\n"
        rv = rv + "            if(indexNum > -1 && indexNum < %d){\n" % len(self.sensor_list)
        rv = rv + "                i2cencoders[indexNum].zero();\n"
        rv = rv + "                Serial.println(\"ok\");\n"
        rv = rv + "            } else {\n"
        rv = rv + "                Serial.println(\"Error: usage - es [id]\");\n"
        rv = rv + "            }\n"
        rv = rv + "        } else {\n"
        rv = rv + "            Serial.println(\"Error: usage - es [id]\");\n"
        rv = rv + "        }\n"
        rv = rv + "    }\n"

        return rv
