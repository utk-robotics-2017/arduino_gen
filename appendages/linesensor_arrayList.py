class linesensor_array:
    def __init__(self, label, pin_list, extra, emitter_pin):
        self.label = label
        self.pin_list = pin_list
        self.extra = extra
        self.emitter_pin = emitter_pin


class linesensor_arrayList:
    def __init__(self):
        self.digital_sensor_list = []
        self.analog_sensor_list = []

    def add(self, json_item):
        if json_item['digital']:
            self.digital_sensor_list.append(linesensor_array(json_item['label'], json_item['pin_list'], json_item['timeout'], json_item['emitter_pin']))
        else:
            self.analog_sensor_list.append(linesensor_array(json_item['label'], json_item['pin_list'], json_item['num_samples'], json_item['emitter_pin']))

    def get_include(self):
        return "#include \"QTRSensors.h\""

    def get_pins(self):
        return ""

    def get_constructor(self):
        rv = ""

        if len(self.digital_sensor_list) > 0:
            for i in range(len(self.digital_sensor_list)):
                rv += "const char {}_index = {};\n".format(self.digital_sensor_list[i].label, i)
            rv += "QTRSensorsRC digital_linsensor_arrays[{}] = {\n".format(len(self.digital_sensor_list))
            for sensor in self.digital_sensor_list:
                rv += "    QTRSensorsRC((unsigned char[]){"
                for pin in sensor.pin_list:
                    rv += "{}, ".format(pin)
                rv = rv[:-2]
                rv += "}, {}, {}, {}),\n".format(len(sensor.pin_list), sensor.extra, sensor.emitter_pin)
            rv = rv[:-2] + "\n};\n"

            for sensor in self.digital_sensor_list:
                rv += "unsigned int {}_sensor_values[{}];\n".format(sensor.label, len(sensor.pin_list))

        if len(self.analog_sensor_list) > 0:
            for i in range(len(self.analog_sensor_list)):
                rv += "const char {}_index = {};\n".format(self.analog_sensor_list[i].label, i)
            rv += "QTRSensorsAnalog analog_linsensor_arrays[{}] = {\n".format(len(self.digital_sensor_list))
            for sensor in self.analog_sensor_list:
                rv += "    QTRSensorsAnalog((unsigned char[]){"
                for pin in sensor.pin_list:
                    rv += "{}, ".format(pin)
                rv = rv[:-2]
                rv += "}, {}, {}, {}),\n".format(len(sensor.pin_list), sensor.extra, sensor.emitter_pin)
            rv = rv[:-2] + "\n};\n"

            for sensor in self.analog_sensor_list:
                rv += "unsigned int {}_sensor_values[{}];\n".format(sensor.label, len(sensor.pin_list))
        return rv

    def get_setup(self):
        rv = "    for (int i = 0; i < 400; i++) { // make the calibration take about 10 seconds\n"
        if len(self.digital_sensor_list) > 0:
            rv += "        for(int j = 0; j < {}; j++) {\n".format(len(self.digital_sensor_list))
            rv += "            digital_linsensor_arrays[j].calibrate();\n"
            rv += "        }\n"

        if len(self.analog_sensor_list) > 0:
            rv += "        for(int j = 0; j < {}; j++) {\n".format(len(self.analog_sensor_list))
            rv += "            analog_linsensor_arrays[j].calibrate();\n"
            rv += "        }\n"
        rv += "    }\n"
        return rv

    # TODO
    def get_response_block(self):
        return ""

    def get_extra_functions(self):
        return ""
