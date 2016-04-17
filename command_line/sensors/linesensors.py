class linesensor:
    def __init__(self, label, pin):
        self.label = label
        self.pin = pin


class linesensors:
    def __init__(self):
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
            rv = rv + "const char %s_pin = %d;\n" % (sensor.label, sensor.pin)
        for sensor in self.analog_sensor_list:
            rv = rv + "const char %s_pin = %d;\n" % (sensor.label, sensor.pin)
        return rv

    def get_constructor(self):
        rv = ""

        if(len(self.digital_sensor_list) > 0):
            for i in range(len(self.digital_sensor_list)):
                rv = rv + "const char %s_index = %d;\n" % (self.digital_sensor_list[i].label, i)

            rv = "char digital_linesensors[%d] = {\n" % (len(self.digital_sensor_list))

            for sensor in self.digital_sensor_list:
                rv = rv + ("    %s_pin,\n") % (sensor.label)

            rv = rv[:-2] + "\n};\n"

        if(len(self.analog_sensor_list) > 0):
            for i in range(len(self.analog_sensor_list)):
                rv = rv + "const char %s_index = %d;\n" % (self.analog_sensor_list[i].label, i)

            rv = "char analog_linesensors[%d] = {\n" % (len(self.analog_sensor_list))

            for sensor in self.analog_sensor_list:
                rv = rv + ("    %s_pin,\n") % (sensor.label)

            rv = rv[:-2] + "\n};\n"

        return rv

    def get_setup(self):
        return ""

    def get_response_block(self):
        rv = ""
        if(len(self.digital_sensor_list) > 0):
            rv = rv + '''    else if(args[0].equals(String("rdls"))){ // read digital linesensors
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                Serial.println(digitalRead(digital_linesensors[indexNum]));
            } else {
                Serial.println("Error: usage - rdls [id]");
            }
        } else {
            Serial.println("Error: usage - rdls [id]");
        }
    }
''' % (len(self.digital_sensor_list))

        if(len(self.analog_sensor_list) > 0):
            rv = rv + '''    else if(args[0].equals(String("rals"))){ // read analog linesensors
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                Serial.println(analogRead(analog_linesensors[indexNum]));
            } else {
                Serial.println("Error: usage - rals [id]");
            }
        } else {
            Serial.println("Error: usage - rals [id]");
        }
    }
''' % (len(self.analog_sensor_list))

        return rv