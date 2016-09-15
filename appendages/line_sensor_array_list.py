from appendages.component_list import ComponentList


class LineSensorArray:
    def __init__(self, label, pin_list, extra, emitter_pin):
        self.label = label
        self.pin_list = pin_list
        self.extra = extra
        self.emitter_pin = emitter_pin


class LineSensorArrayList(ComponentList):
    TIER = 1

    def __init__(self):
        self.digital_sensor_list = []
        self.analog_sensor_list = []

    def add(self, json_item):
        if json_item['digital']:
            self.digital_sensor_list.append(LineSensorArray(json_item['label'],
                                                            json_item['pin_list'],
                                                            json_item['timeout'],
                                                            json_item['emitter_pin']))
        else:
            self.analog_sensor_list.append(LineSensorArray(json_item['label'],
                                                           json_item['pin_list'],
                                                           json_item['num_samples'],
                                                           json_item['emitter_pin']))

    def get_includes(self):
        return "#include \"QTRSensors.h\""

    def get_constructor(self):
        rv = ""
        if len(self.digital_sensor_list) > 0:
            for i, sensor in enumerate(self.digital_sensor_list):
                rv += "const char {0:s}_index = {1:d};\n".format(sensor.label, i)
            rv += "QTRSensorsRC digital_linsensor_arrays[{0:d}] = {{\n".format(len(self.digital_sensor_list))
            for sensor in self.digital_sensor_list:
                rv += "\tQTRSensorsRC((unsigned char[]){"
                for pin in sensor.pin_list:
                    rv += "{0:d}, ".format(pin)
                rv = rv[:-2]
                rv += "}}, {0:d}, {1:d}, {2:d}),\n".format(len(sensor.pin_list), sensor.extra, sensor.emitter_pin)
            rv = rv[:-2] + "\n};\n"

            rv += "unsigned int digital_linesensor_values_arrays[{0:d}][] = {{\n".format(len(self.digital_sensor_list))
            for sensor in self.digital_sensor_list:
                rv += "unsigned int [{1:d}],\n".format(sensor.label, len(sensor.pin_list))
            rv = rv[:-2] + "\n};\n"

        if len(self.analog_sensor_list) > 0:
            for i, sensor in enumerate(self.analog_sensor_list):
                rv += "const char {0:s}_index = {1:d};\n".format(sensor.label, i)
                rv += "QTRSensorsAnalog analog_linsensor_arrays[{0:d}] = {\n".format(len(self.digital_sensor_list))
            for sensor in self.analog_sensor_list:
                rv += "\tQTRSensorsAnalog((unsigned char[]){"
                for pin in sensor.pin_list:
                    rv += "{0:d}, ".format(pin)
                rv = rv[:-2]
                rv += "}}, {0:d}, {1:d}, {2:d}),\n".format(len(sensor.pin_list), sensor.extra, sensor.emitter_pin)
            rv = rv[:-2] + "\n};\n"

            rv += "unsigned int analog_linesensor_values_arrays[{0:d}][] = {{\n".format(len(self.analog_sensor_list))
            for sensor in self.analog_sensor_list:
                rv += "unsigned int [{1:d}],\n".format(sensor.label, len(sensor.pin_list))
            rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        rv = "\tfor (int i = 0; i < 400; i++) { // make the calibration take about 10 seconds\n"
        if len(self.digital_sensor_list) > 0:
            rv += "\t\tfor(int j = 0; j < {0:d}; j++) {{\n".format(len(self.digital_sensor_list))
            rv += "\t\t\tdigital_linesensor_arrays[j].calibrate();\n"
            rv += "\t\t}\n"

        if len(self.analog_sensor_list) > 0:
            rv += "\t\tfor(int j = 0; j < {0:d}; j++) {\n".format(len(self.analog_sensor_list))
            rv += "\t\t\tanalog_linesensor_arrays[j].calibrate();\n"
            rv += "\t}\n"
        rv += "\t}\n"
        return rv

    # TODO
    def get_response_block(self):
        return """\t\telse if(args[0].equals(String("rdlsa"))){{ // read digital line sensor array
        if(numArgs == 3){{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}){{
                int white = args[2].toInt();
                if(white > -1 && white < 2){{
                    Serial.println(digital_linesensor_array[indexNum].readline(digital_linesensor_values_arrays[indexNum], 1, white));
                }} else {{
                    Serial.println("Error: usage - rdlsa [id] [white]");
                }}
            }} else {{
                Serial.println("Error: usage - rdlsa [id] [white]");
            }}
        }} else {{
            Serial.println("Error: usage - rdlsa [id] white");
        }}
    }}"""
