class MonsterMotorMotor:
    def __init__(self, label, inA_pin, inB_pin, pwm_pin, reverse):
        self.label = label
        self.inA_pin = inA_pin
        self.inB_pin = inB_pin
        self.pwm_pin = pwm_pin
        self.reverse = reverse


class Rover5Motor:
    def __init__(self, label, dir_pin, pwm_pin, reverse):
        self.label = label
        self.dir_pin = dir_pin
        self.pwm_pin = pwm_pin
        self.reverse = reverse


class motorList:
    def __init__(self):
        self.monsterMotos = dict()
        self.rover5s = dict()

    def add(self, json_item):
        if json_item['motorController'].lower() == 'monsterMoto':
            self.monsterMotos[json_item['label']] = MonsterMotorMotor(json_item['label'], json_item['inA_pin'], json_item['inB_pin'], json_item['pwm_pin'], json_item['reverse'])
        elif json_item['motorController'].lower() == 'roverFive':
            self.rover5s[json_item['label']] = Rover5Motor(json_item['label'], json_item['dir_pin'], json_item['pwm_pin'], json_item['reverse'])

    def get(self, label):
        if label in self.monsterMotos:
            return self.monsterMotos[label]
        elif label in self.rover5s:
            return self.rover5s[label]

    def get_include(self):
        return "#include \"Motor.h\""

    def get_include_files(self):
        return ['Motor.h', 'Motor.cpp']

    def get_pins(self):
        return ""

    def get_constructor(self):
        rv = ""
        for i, label in zip(range(len(self.monsterMotos)), self.monsterMotos.keys()):
            rv += "const char %s_index = %d;\n" % (label, i)
        rv += "Motor motors[%d] = {\n" % (len(self.monsterMotos) + len(self.rover5s))
        for motor in self.monsterMotos.values():
            rv += "    Motor(%d, %d, %d, %d, MonsterMoto),\n" % (motor.inA_pin, motor.inB_pin, motor.pwm_pin, 1 if motor.reverse else 0)
        for motor in self.rover5s.values():
            rv += "    Motor(%d, -1, %d, %d, RoverFive),\n" % (motor.dir_pin, motor.pwm_pin, 1 if motor.reverse else 0)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        return ""

    def get_loop_functions(self):
        return ""

    def get_response_block(self):
        length = len(self.monsterMotos) + len(self.rover5s)
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
