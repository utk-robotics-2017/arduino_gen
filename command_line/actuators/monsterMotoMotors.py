class monsterMotoMotor:
    def __init__(self, label, inA_pin, inB_pin, pwm_pin, reverse):
        self.label = label
        self.inA_pin = inA_pin
        self.inB_pin = inB_pin
        self.pwm_pin = pwm_pin
        self.reverse = reverse


class monsterMotoMotors:
    def __init__(self):
        self.motor_list = []

    def add(self, json_item):
        self.motor_list.append(monsterMotoMotor(json_item['label'], json_item['inA_pin'], json_item['inB_pin'], json_item['pwm_pin'], json_item['reverse']))

    def get_include(self):
        return ""

    def get_pins(self):
        rv = ""
        for motor in self.motor_list:
            rv = rv + "const char %s_inA_pin = %d;\n" % (motor.label, motor.inA_pin)
            rv = rv + "const char %s_inB_pin = %d;\n" % (motor.label, motor.inB_pin)
            rv = rv + "const char %s_pwm_pin = %d;\n" % (motor.label, motor.pwm_pin)
        return rv

    def get_constructor(self):
        rv = ""
        for i in range(len(self.motor_list)):
            rv = rv + "const char %s_index = %d;\n" % (self.motor_list[i].label, i)

        rv = rv + "char inA_pins[%d]= {\n" % len(self.motor_list)
        for motor in self.motor_list:
            rv = rv + "    %s_inA_pin,\n" % motor.label
        rv = rv[:-2] + "\n};\n"

        rv = rv + "char inB_pins[%d]= {\n" % len(self.motor_list)
        for motor in self.motor_list:
            rv = rv + "    %s_inB_pin,\n" % motor.label
        rv = rv[:-2] + "\n};\n"

        rv = rv + "char pwm_pins[%d]= {\n" % len(self.motor_list)
        for motor in self.motor_list:
            rv = rv + "    %s_pwm_pin,\n" % motor.label
        rv = rv[:-2] + "\n};\n"

        rv = rv + "char reverse[%d]= {\n" % len(self.motor_list)
        for motor in self.motor_list:
            rv = rv + "    %d,\n" % 1 if motor.reverse else 0
        rv = rv[:-2] + "\n};\n"

        return rv

    def get_setup(self):
        return '''    for(int i = 0; i < %d; i++) {
        pinMode(inA_pins[i], OUTPUT);
        pinMode(inB_pins[i], OUTPUT);
        pinMode(pwm_pins[i], OUTPUT);
    }
    // Initialize braked
    for(int i = 0; i < %d; i++) {
        digitalWrite(inA_pins[i], LOW);
        digitalWrite(inB_pins[i], LOW);
    }
''' % (len(self.motor_list), len(self.motor_list))

    def get_response_block(self):
        return '''    else if(args[0].equals(String("mod"))){ // motor drive
        if(numArgs ==  3) {
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d) {
                int value = args[2].toInt();
                if( value < -1023 || value > 1023) {
                    Serial.println("Error: usage - mod [id] [value]");
                } else {
                    if(reverse[indexNum] == 1) {
                        value = value * -1;
                    }

                    if(value == 0) {
                        digitalWrite(inA_pins[indexNum], LOW);
                        digitalWrite(inB_pins[indexNum], LOW);
                        analogWrite(pwm_pins[indexNum], 0);
                    } else if(value > 0) {
                        digitalWrite(inA_pins[indexNum], HIGH);
                        digitalWrite(inB_pins[indexNum], LOW);
                        analogWrite(pwm_pins[indexNum], value);
                    } else {
                        digitalWrite(inA_pins[indexNum], LOW);
                        digitalWrite(inB_pins[indexNum], HIGH);
                        analogWrite(pwm_pins[indexNum], -1 * value);
                    }
                }
            } else {
                Serial.println("Error: usage - mod [id] [value]");
            }
        } else {
            Serial.println("Error: usage - mod [id] [value]");
        }
    }
    else if(args[0].equals(String("mos"))){ // motor stop
        if(numArgs == 2) {
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d) {
                digitalWrite(inA_pins[indexNum], LOW);
                digitalWrite(inB_pins[indexNum], LOW);
                analogWrite(pwm_pins[indexNum], 0);
            } else {
                Serial.println("Error: usage - mos [id]");
            }
        } else {
            Serial.println("Error: usage - mos [id]");
        }
    }

''' % (len(self.motor_list), len(self.motor_list))
