class linesensor_array:
    def __init__(self, label, pin_list, extra, emitter_pin):
        self.label = label
        self.pin_list = pin_list
        self.extra = extra
        self.emitter_pin = emitter_pin


class linesensor_arrays:
    def __init__(self):
        self.digital_sensor_list = []
        self.analog_sensor_list = []

    def add(self, json_item):
        if json_item['digital']:
            self.digital_sensor_list.append(linesensor_array(json_item['label'], json_item['pin_list']))
        else:
            self.analog_sensor_list.append(linesensor_array(json_item['label'], json_item['pin_list']))

    def get_include(self):
        return "#include \"QTRSensors.h\";\n"

    def get_pins(self):
        return ""

    def get_constructor(self):
        rv = ""

        for i in range(len(self.digital_sensor_list)):
            rv = rv + "const char %s_index = %d;\n" % (self.digital_sensor_list[i].label, i)
        rv = rv + "QTRSensorsRC digital_linsensor_arrays[%d] = {\n" % len(self.digital_sensor_list)
        for sensor in self.digital_sensor_list:
            rv = rv + "    QTRSensorsRC((unsigned char[]){"
            for pin in sensor.pin_list:
                rv = rv + "%d, " % pin
            rv = rv[:-2]
            rv = rv + "}, %d),\n" % len(sensor.pin_list)
        rv = rv[:-2] + "\n};\n"


        for i in range(len(self.analog_sensor_list)):
            rv = rv + "const char %s_index = %d;\n" % (self.analog_sensor_list[i].label, i)
        rv = rv + "QTRSensorsAnalog analog_linsensor_arrays[%d] = {\n" % len(self.digital_sensor_list)
        for sensor in self.analog_sensor_list:
            rv = rv + "    QTRSensorsAnalog((unsigned char[]){"
            for pin in sensor.pin_list:
                rv = rv + "%d, " % pin
            rv = rv[:-2]
            rv = rv + "}, %d),\n" % len(sensor.pin_list)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        return ""

    def get_response_block(self):
        return ""
