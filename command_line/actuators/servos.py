class servo:
    def __init__(self, label, pin):
        self.label = label
        self.pin = pin


class servos:
    def __init__(self):
        self.actuator_list = []

    def add(self, json_item):
        self.actuator_list.append(servo(json_item['label'], json_item['pin']))

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
            rv += "    servos[%s_index].attach(%s_pin);\n" % (actuator.label, actuator.label)
        rv += "\n"

        rv += "char servo_pins[%d] = {\n" % (len(self.actuator_list))
        for actuator in self.actuator_list:
            rv += ("    %s_pin,\n") % (sensor.label)
        rv = rv[:-2] + "\n};\n"

        return rv

#TODO: add in attach and detach

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
''' % (len(self.actuator_list))
