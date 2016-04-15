class linesensor:
    def __init__(self, label, pin):
        self.label = label
        self.pin = pin


class linesensors:
    def __init__(self):
        self.sensor_list = []

    def add(self, label, pin):
        self.sensor_list.append(linesensor(label, pin))

    def get_include(self):
        return ""

    def get_pins(self):
        rv = ""
        for sensor in self.sensor_list:
            rv = rv + "const char %s_pin = %d;\n" % (sensor.label, sensor.pin)
        return rv

    def get_constructor(self):
        rv = ""

        for i in range(len(self.sensor_list)):
            rv = rv + "const char %s_index = %d;\n" % (self.sensor_list[i].label, i)

        rv = "char linesensors[%d] = {\n" % (len(self.sensor_list))

        for sensor in self.sensor_list:
            rv = rv + ("    %s_pin,\n") % (sensor.label)

        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        return ""

    def get_response_block(self):
        rv = '''    else if(args[0].equals(String("rls"))){ // read linesensors
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                Serial.println(analogRead(linesensors[indexNum]));
            } else {
                Serial.println("Error: usage - rls [id]");
            }
        } else {
            Serial.println("Error: usage - rls [id]");
        }
    }
''' % (len(self.sensor_list))
        return rv
