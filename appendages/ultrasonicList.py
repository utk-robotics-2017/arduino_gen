class ultrasonic:
    def __init__(self, label, pin):
        self.label = label
        self.pin = pin


class ultrasonicList:

    def __init__(self):
        self.tier = 1
        self.sensor_list = []

    def add(self, json_item):
        self.sensor_list.append(ultrasonic(json_item['label'], json_item['pin']))

    def get_include(self):
        return "#include \"NewPing.h\""

    def get_pins(self):
        rv = ""
        for sensor in self.sensor_list:
            rv += "const char {0:s}_pin = {0:d};\n".format(sensor.label, sensor.pin)
        return rv

    def get_constructor(self):
        rv = ""
        for i, sensor in enumerate(self.sensor_list):
            rv += "const char {0:s}_index = {1:d};\n".format(sensor.label, i)
        rv += "NewPing ultrasonics[{0:d}] = {\n".format(len(self.sensor_list))

        for sensor in self.sensor_list:
            rv += "\tNewPing({0:s}_pin, {0:s}_pin),\n".format(sensor.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        return ""

    def get_loop_functions(self):
        return ""

    def get_response_block(self):
        return '''\t\telse if(args[0].equals(String("rus"))){{ // read ultrasonics
        if(numArgs == 2){{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}){{
                unsigned int response = ultrasonics[indexNum].ping();
                Serial.println(response);
            }} else {{
                Serial.println("Error: usage - rus [id]");
            }}
        }} else {{
            Serial.println("Error: usage - rus [id]");
        }}
    }}
'''.format(len(self.sensor_list))

    def get_extra_functions(self):
        return ""

    def get_indices(self):
        for i, ultrasonic in enumerate(self.sensor_list):
            yield i, ultrasonic
