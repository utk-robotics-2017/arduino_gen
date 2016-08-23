class servo:
    def __init__(self, label, pin):
        self.label = label
        self.pin = pin


class servoList:
    def __init__(self):
        self.actuators = dict()

    def add(self, json_item):
        self.actuators[json_item['label']] = servo(json_item['label'], json_item['pin'])

    def get(self, label):
        return self.actuators[label]

    def get_include(self):
        return "#include \"Servo.h\";"

    def get_include_files(self):
        return []

    def get_pins(self):
        rv = ""
        for actuator in self.actuators.values():
            rv = rv + "const char %s_pin = %d;\n" % (actuator.label, actuator.pin)
        return rv

    def get_constructor(self):
        rv = ""
        for i, label in zip(range(len(self.actuators)), self.actuators.keys()):
            rv = rv + "const char %s_index = %d;\n" % (label, i)

        rv += "char servo_pins[%d] = {\n" % (len(self.actuators))
        for label in self.actuators.keys():
            rv += ("    %s_pin,\n") % (label)
        rv = rv[:-2] + "\n};\n"

        rv = rv + ("Servo servos[%d];\n") % (len(self.actuators))
        return rv

    def get_setup(self):
        rv = ""
        for label in self.actuators.keys():
            rv += "    servos[%s_index].attach(%s_pin);\n" % (label, label)
        rv += "\n"

        return rv

    def get_loop_functions(self):
        return ""

    def get_response_block(self):
        return '''    else if(args[0].equals(String("ss"))){ // set servo
        if(numArgs == 3){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                int value = args[2].toInt();
                if(!servos[indexNum].attached()){
                    servos[indexNum].attach(servo_pins[indexNum]);
                }
                servos[indexNum].write(value);
                Serial.println("ok");
            } else {
                Serial.println("Error: usage - ss [id] [value]");
            }
        } else {
            Serial.println("Error: usage - ss [id] [value]");
        }
    }
    else if(args[0].equals(String("sd"))){ // detach servo
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                servos[indexNum].detach();
                Serial.println("ok");
            } else {
                Serial.println("Error: usage - sd [id]");
            }
        } else {
            Serial.println("Error: usage - sd [id]");
        }
    }
''' % (len(self.actuators), len(self.actuators))

    def get_extra_functions(self):
        return ""
