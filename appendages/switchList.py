class switch:
    def __init__(self, label, pin, pullup):
        self.label = label
        self.pin = pin
        self.pullup = pullup


class switchList:
    def __init__(self):
        self.sensor_list = []

    def add(self, json_item):
        self.sensor_list.append(switch(json_item['label'], json_item['pin'], json_item['pullup']))

    def get_include(self):
        return ""

    def get_include_files(self):
        return []

    def get_pins(self):
        rv = ""
        for sensor in self.sensor_list:
            rv = rv + "const char %s_pin = %d;\n" % (sensor.label, sensor.pin)
        return rv

    def get_constructor(self):
        rv = ""
        for i in range(len(self.sensor_list)):
            rv = rv + "const char %s_index = %d;\n" % (self.sensor_list[i].label, i)
        rv = rv + "char switches[%d] = {\n" % (len(self.sensor_list))
        for sensor in self.sensor_list:
            rv = rv + ("    %s_pin,\n") % (sensor.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        rv = ""
        for sensor in self.sensor_list:
            if sensor.pullup:
                rv = rv + "    pinMode(%s_pin, INPUT_PULLUP);\n" % sensor.label
            else:
                rv = rv + "    pinMode(%s_pin, INPUT);\n" % sensor.label
        rv = rv + "\n"
        return rv

    def get_loop_functions(self):
        return ""

    def get_response_block(self):
        return '''    else if(args[0].equals(String("rs"))){ // read switches
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                Serial.println(digitalRead(switches[indexNum]));
            } else {
                Serial.println("Error: usage - rs [id]");
            }
        } else {
            Serial.println("Error: usage - rs [id]");
        }
    }
''' % (len(self.sensor_list))

    def get_extra_functions(self):
        return ""
