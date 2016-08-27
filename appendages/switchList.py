class Switch:
    def __init__(self, label, pin, pullup):
        self.label = label
        self.pin = pin
        self.pullup = pullup


class switchList:
    def __init__(self):
        self.switchList = []

    def add(self, json_item):
        self.switchList.append(Switch(json_item['label'], json_item['pin'], json_item['pullup']))
        self.switchList.sort(key=lambda x: x.label, reverse=False)

    def get_include(self):
        return ""

    def get_include_files(self):
        return []

    def get_pins(self):
        rv = ""
        for sensor in self.switchList:
            rv = rv + "const char %s_pin = %d;\n" % (sensor.label, sensor.pin)
        return rv

    def get_constructor(self):
        rv = ""
        for i, sensor in enumerate(self.switchList):
            rv += "const char %s_index = %d;\n" % (sensor.label, i)
        rv += "char switches[%d] = {\n" % (len(self.switchList))
        for sensor in self.switchList:
            rv += ("    %s_pin,\n") % (sensor.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        rv = ""
        for sensor in self.switchList:
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
''' % (len(self.switchList))

    def get_extra_functions(self):
        return ""
