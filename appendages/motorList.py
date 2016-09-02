class Motor:
    def __init__(self, label, inA_pin, inB_pin, pwm_pin, reverse, motor_controller):
        self.label = label
        self.inA_pin = inA_pin
        self.inB_pin = inB_pin
        self.pwm_pin = pwm_pin
        self.reverse = reverse
        self.motor_controller = motor_controller

class motorList:
    def __init__(self):
        self.tier = 1
        self.motorDict = {}
        self.motorList = []

    def add(self, json_item):
        if json_item['motorController'].lower() == 'monstermoto':
            motor = Motor(json_item['label'], json_item['inA_pin'], json_item['inB_pin'], json_item['pwm_pin'], json_item['reverse'], 'MonsterMoto')
        elif json_item['motorController'].lower() == 'roverfive':
            motor = Motor(json_item['label'], json_item['dir_pin'], -1, json_item['pwm_pin'], json_item['reverse'], 'RoverFive')

        self.motorDict[motor.label] = motor
        self.motorList.append(motor)
        self.motorList.sort(key=lambda x: x.label, reverse=False)

    def get(self, label):
        if label in self.motorDict:
            return self.motorDict[label]

    def get_include(self):
        return "#include \"Motor.h\""

    def get_pins(self):
        return ""

    def get_constructor(self):
        rv = ""
        for i, motor in enumerate(self.motorList):
            rv += "const char %s_index = %d;\n" % (motor.label, i)
        rv += "Motor motors[%d] = {\n" % (len(self.motorList))
        for motor in self.motorList:
            rv += "    Motor(%d, %d, %d, %d, %s),\n" % (motor.inA_pin, motor.inB_pin, motor.pwm_pin, 1 if motor.reverse else 0, motor.motor_controller)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        rv = ""
        for motor in self.motorList:
            rv += "    pinMode(%d, OUTPUT);\n" % motor.inA_pin
            if not motor.inB_pin == -1:
                rv += "    pinMode(%d, OUTPUT);\n" % motor.inB_pin
            rv += "    pinMode(%d, OUTPUT);\n" % motor.pwm_pin
        return rv

    def get_loop_functions(self):
        return ""

    def get_response_block(self):
        length = len(self.motorList)
        return '''    else if(args[0].equals(String("mod"))){ // motor drive
        if(numArgs ==  3) {
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d) {
                int value = args[2].toInt();
                if( value < -1023 || value > 1023) {
                    Serial.println("Error: usage - mod [id] [value]");
                } else {
                    motors[indexNum].drive(value);
                    Serial.println("ok");
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
                motors[indexNum].stop();
                Serial.println("ok");
            } else {
                Serial.println("Error: usage - mos [id]");
            }
        } else {
            Serial.println("Error: usage - mos [id]");
        }
    }
''' % (length, length)

    def get_extra_functions(self):
        return ""

    def get_indices(self):
        for i, motor in enumerate(self.motorList):
            yield i, motor
