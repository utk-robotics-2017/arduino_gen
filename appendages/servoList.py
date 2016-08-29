class Servo:
    def __init__(self, label, pin):
        self.label = label
        self.pin = pin


class servoList:
    def __init__(self):
        self.tier = 1
        self.servoDict = {}
        self.servoList = []

    def add(self, json_item):
        servo = Servo(json_item['label'], json_item['pin'])
        self.servoDict[servo.label] = servo
        self.servoList.append(servo)
        self.servoList.sort(key=lambda x: x.label, reverse=False)

    def get(self, label):
        return self.servoDict[label]

    def get_include(self):
        return "#include \"Servo.h\""

    def get_include_files(self):
        return []

    def get_pins(self):
        rv = ""
        for actuator in self.servoList:
            rv = rv + "const char %s_pin = %d;\n" % (actuator.label, actuator.pin)
        return rv

    def get_constructor(self):
        rv = ""
        for i, servo in enumerate(self.servoList):
            rv += "const char %s_index = %d;\n" % (servo.label, i)

        rv += "char servo_pins[%d] = {\n" % (len(self.servoList))
        for servo in self.servoList:
            rv += ("    %s_pin,\n") % (servo.label)
        rv = rv[:-2] + "\n};\n"

        rv = rv + ("Servo servos[%d];\n") % (len(self.servoList))
        return rv

    def get_setup(self):
        rv = ""
        for servo in self.servoList:
            rv += "    servos[%s_index].attach(%s_pin);\n" % (servo.label, servo.label)
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
''' % (len(self.servoList), len(self.servoList))

    def get_extra_functions(self):
        return ""
