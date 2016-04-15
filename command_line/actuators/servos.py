class servo:
    def __init__(self, label, pin):
        self.label = label
        self.pin = pin


class servos:
    def __init__(self):
        self.actuator_list = []

    def add(self, label, pin):
        self.actuator_list.append(servo(label, pin))

    def get_include(self):
        return "#include \"Servo.h\";"

    def get_pins(self):
        rv = ""
        for actuator in self.actuator_list:
            rv = rv + "const char %s_pin = %d;\n" % (actuator.label, actuator.pin)
        return rv

    def get_constructor(self):
        rv = ""
        for i in range(len(self.actuator_list)):
            rv = rv + "const char %s_index = %d;\n" % (self.actuator_list[i].label, i)
        rv = rv + ("Servo servos[%d];\n") % (len(self.actuator_list))
        return rv

    def get_setup(self):
        rv = ""
        for actuator in self.actuator_list:
            rv = rv + "    servos[%s_index].attach(%s_pin);\n" % (actuator.label, actuator.label)
        rv = rv + "\n"
        return rv

#TODO: add in attach and detach

    def get_response_block(self):
        rv = '''    else if(args[0].equals(String("ss"))){ // set servo
        if(numArgs == 3){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                int value = args[2].toInt();
                servos[indexNum].write(value);
                Serial.println("ok");
            } else {
                Serial.println("Error: usage - ss [id] [value]");
            }
        } else {
            Serial.println("Error: usage - ss [id] [value]");
        }
    }
''' % (len(self.actuator_list))
        return rv
