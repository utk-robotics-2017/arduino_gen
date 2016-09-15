from appendages.component_list import ComponentList


class I2CEncoder:
    def __init__(self, label, reverse, init_number):
        self.label = label
        self.reverse = reverse
        self.init_number = init_number


class I2CEncoderList(ComponentList):
    TIER = 1

    def __init__(self):
        self.sensors = dict()
        self.sorted_sensors = []

    def add(self, json_item):
        sensor = I2CEncoder(json_item['label'], json_item['reverse'], json_item['init_number'])
        self.sensors[json_item['label']] = sensor
        self.sorted_sensors.append(sensor)
        self.sorted_sensors.sort(key=lambda x: x.init_number, reverse=False)

    def get(self, label):
        if label in self.sensors:
            return self.sensors[label]
        else:
            return None

    def get_includes(self):
        return "#include <Wire.h>\n#include \"I2CEncoder.h\""

    def get_constructor(self):
        rv = ""
        for i in range(len(self.sorted_sensors)):
            rv += "const char {0:s}_index = {1:d};\n".format(self.sorted_sensors[i].label, i)
            rv += "I2CEncoder i2cencoders[{0:d}];\n".format(len(self.sorted_sensors))
        return rv

    def get_setup(self):
        rv = "    Wire.begin();\n"
        for sensor in self.sorted_sensors:
            rv += ("\ti2cencoders[{0:s}_index].init(MOTOR_393_TORQUE_ROTATIONS, " +
                   "MOTOR_393_TIME_DELTA);\n").format(sensor.label)
        for sensor in self.sorted_sensors:
            if sensor.reverse:
                rv += "\ti2cencoders[{0:s}_index].setReversed(true);\n".format(sensor.label)
        for sensor in self.sorted_sensors:
            rv += "\ti2cencoders[{0:s}_index].zero();\n".format(sensor.label)
        rv += "\n"
        return rv

    def get_response_block(self):
        numSensors = len(self.sorted_sensors)

        return '''\t\telse if(args[0].equals(String("ep"))){{ // i2c encoder position (in rotations)
        if(numArgs == 2){{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}){{
                char dts[256];
                dtostrf(i2cencoders[indexNum].getPosition(), 0, 6, dts);
                Serial.println(dts);
            }} else {{
                Serial.println("Error: usage - ep [id]");
            }}
        }} else {{
            Serial.println("Error: usage - ep [id]");
        }}
    }}
    else if(args[0].equals(String("erp"))){{ // i2c encoder raw position (in ticks)
        if(numArgs == 2){{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}){{
                char dts[256];
                dtostrf(i2cencoders[indexNum].getRawPosition(), 0, 6, dts);
                Serial.println(dts);
            }} else {{
                Serial.println("Error: usage - erp [id]");
            }}
        }} else {{
            Serial.println("Error: usage - erp [id]");
        }}
    }}
    else if(args[0].equals(String("es"))){{ // i2c encoder speed (in revolutions per minute)
        if(numArgs == 2){{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}){{
                char dts[256];
                dtostrf(i2cencoders[indexNum].getSpeed(), 0, 6, dts);
                Serial.println(dts);
            }} else {{
                Serial.println("Error: usage - es [id]");
            }}
        }} else {{
            Serial.println("Error: usage - es [id]");
        }}
    }}
    else if(args[0].equals(String("ev"))){{ // i2c encoder velocity (in revolutions per minute)
        if(numArgs == 2){{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}){{
                char dts[256];
                dtostrf(i2cencoders[indexNum].getVelocity(), 0, 6, dts);
                Serial.println(dts);
            }} else {{
                Serial.println("Error: usage - ev [id]");
            }}
        }} else {{
            Serial.println("Error: usage - ev [id]");
        }}
    }}
    else if(args[0].equals(String("ez"))){{ // i2c encoder zero
        if(numArgs == 2){{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}){{
                i2cencoders[indexNum].zero();
                Serial.println("ok");
            }} else {{
                Serial.println("Error: usage - ez [id]");
            }}
        }} else {{
            Serial.println("Error: usage - ez [id]");
        }}
    }}
'''.format(numSensors)

    def get_indices(self):
        for i, i2cencoder in enumerate(self.sorted_sensors):
            yield i, i2cencoder
