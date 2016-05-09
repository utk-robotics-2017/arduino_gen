class MonsterMotorMotor:
    def __init__(self, label, inA_pin, inB_pin, pwm_pin, reverse):
        self.label = label
        self.inA_pin = inA_pin
        self.inB_pin = inB_pin
        self.pwm_pin = pwm_pin
        self.reverse = reverse


class motors:
    def __init__(self):
        self.monsterMotos = dict()

    def add(self, json_item):
        if json_item['motorController'].lower() == 'monstermoto':
            self.monsterMotos[json_item['label']] = MonsterMotorMotor(json_item['label'], json_item['inA_pin'], json_item['inB_pin'], json_item['pwm_pin'], json_item['reverse'])

    def get(self, label):
        if label in self.monsterMotos:
            return self.monsterMotos[label]

    def get_include(self):
        return "#include \"Motor.h\";"

    def get_pins(self):
        return ""

    def get_constructor(self):
        rv = ""
        for i, label in zip(range(len(self.monsterMotos)), self.monsterMotos.keys()):
            rv += "const char %s_index = %d;\n" % (label, i)
        rv += "Motor motors[%d] = {\n" % len(self.monsterMotos)
        for motor in self.monsterMotos.values():
            rv += "    Motor(%d, %d, %d, %d, MonsterMoto),  // %s\n" % (motor.inA_pin, motor.inB_pin, motor.pwm_pin, 1 if motor.reverse else 0, motor.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        return ""

    def get_loop_functions(self):
        return ""

    def get_response_block(self):
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
            } else {
                Serial.println("Error: usage - mos [id]");
                Serial.println("ok");
            }
        } else {
            Serial.println("Error: usage - mos [id]");
        }
    }
''' % (len(self.monsterMotos), len(self.monsterMotos))

    def get_extra_functions(self):
        return ""