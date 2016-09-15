class linesensor:
    def __init__(self, label, pin):
        self.label = label
        self.pin = pin


class linesensorList:
    def __init__(self):
        self.tier = 1
        self.digital_sensor_list = []
        self.analog_sensor_list = []

    def add(self, json_item):
        if(json_item['digital']):
            self.digital_sensor_list.append(linesensor(json_item['label'], json_item['pin']))
        else:
            self.analog_sensor_list.append(linesensor(json_item['label'], json_item['pin']))

    def get_include(self):
        return ""

    def get_pins(self):
        rv = ""
        for sensor in self.digital_sensor_list:
            rv += "const char {0:s}_pin = {1:d};\n".format(sensor.label, sensor.pin)
        for sensor in self.analog_sensor_list:
            rv += "const char {0:s}_pin = {1:d};\n".format(sensor.label, sensor.pin)
        return rv

    def get_constructor(self):
        rv = ""

        if(len(self.digital_sensor_list) > 0):
            for i, linesensor in enumerate(self.digital_sensor_list):
                rv += "const char {0:s}_index = {0:d};\n".format(linesensor.label, i)

            rv += "char digital_linesensors[{0:d}] = \{\n".format(len(self.digital_sensor_list))

            for sensor in self.digital_sensor_list:
                rv += ("\t{0:s}_pin,\n").format(sensor.label)

            rv = rv[:-2] + "\n};\n"

        if(len(self.analog_sensor_list) > 0):
            for i, linesensor in enumerate(self.analog_sensor_list):
                rv += "const char {0:s}_index = {1:d};\n".format(linesensor.label, i)

            rv += "char analog_linesensors[{0:d}] = {\n".format(len(self.analog_sensor_list))

            for sensor in self.analog_sensor_list:
                rv += ("\t{0:s}_pin,\n").format(sensor.label)

            rv = rv[:-2] + "\n};\n"

        return rv

    def get_setup(self):
        return ""

    def get_loop_functions(self):
        return ""

    def get_response_block(self):
        rv = ""
        if(len(self.digital_sensor_list) > 0):
            rv += '''\t\telse if(args[0].equals(String("rdls"))){{ // read digital linesensors
        if(numArgs == 2){{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}){{
                Serial.println(digitalRead(digital_linesensors[indexNum]));
            }} else {{
                Serial.println("Error: usage - rdls [id]");
            }}
        }} else {{
            Serial.println("Error: usage - rdls [id]");
        }}
    }}
'''.format(len(self.digital_sensor_list))

        if(len(self.analog_sensor_list) > 0):
            rv += '''\t\telse if(args[0].equals(String("rals"))){{ // read analog linesensors
        if(numArgs == 2){{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}){{
                Serial.println(analogRead(analog_linesensors[indexNum]));
            }} else {{
                Serial.println("Error: usage - rals [id]");
            }}
        }} else {{
            Serial.println("Error: usage - rals [id]");
        }}
    }}
'''.format(len(self.analog_sensor_list))

        return rv

    def get_extra_functions(self):
        return ""

    def get_indices(self):
        for i, linesensor in enumerate(self.digital_sensor_list):
            yield i, linesensor
        for i, linesensor in enumerate(self.analog_sensor_list):
            yield i, linesensor
