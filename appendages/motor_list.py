from appendages.component_list import ComponentList


class Motor:
    def __init__(self, label, inA_pin, inB_pin, pwm_pin, reverse, motor_controller):
        self.label = label
        self.inA_pin = inA_pin
        self.inB_pin = inB_pin
        self.pwm_pin = pwm_pin
        self.reverse = reverse
        self.motor_controller = motor_controller


class MotorList(ComponentList):
    TIER = 1

    def __init__(self):
        self.motorDict = {}
        self.motorList = []

    def add(self, json_item):
        if json_item['motorController'].lower() == 'monstermoto':
            motor = Motor(json_item['label'], json_item['inA_pin'], json_item['inB_pin'],
                          json_item['pwm_pin'], json_item['reverse'], 'MonsterMoto')
        elif json_item['motorController'].lower() == 'roverfive':
            motor = Motor(json_item['label'], json_item['dir_pin'], -1, json_item['pwm_pin'],
                          json_item['reverse'], 'RoverFive')

        self.motorDict[motor.label] = motor
        self.motorList.append(motor)
        self.motorList.sort(key=lambda x: x.label, reverse=False)

    def get(self, label):
        if label in self.motorDict:
            return self.motorDict[label]
        else:
            return None

    def get_includes(self):
        return "#include \"Motor.h\""

    def get_constructor(self):
        rv = ""
        for i, motor in enumerate(self.motorList):
            rv += "const char {0:s}_index = {1:d};\n".format(motor.label, i)
        rv += "Motor motors[{0:d}] = {{\n".format(len(self.motorList))
        for motor in self.motorList:
            rv += "\tMotor({0:d}, {1:d}, {2:d}, {3:d}, {4:s}),\n"\
                    .format(motor.inA_pin, motor.inB_pin, motor.pwm_pin, 1 if motor.reverse else 0,
                            motor.motor_controller)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        rv = ""
        for motor in self.motorList:
            rv += "pinMode({0:d}, OUTPUT);\n".format(motor.inA_pin)
            if not motor.inB_pin == -1:
                rv += "pinMode({0:d}, OUTPUT);\n".format(motor.inB_pin)
            rv += "pinMode({0:d}, OUTPUT);\n".format(motor.pwm_pin)
        return rv

    def get_response_block(self):
        length = len(self.motorList)
        return '''\t\telse if(args[0].equals(String("mod"))){{ // motor drive
        if(numArgs ==  3) {{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}) {{
                int value = args[2].toInt();
                if( value < -1023 || value > 1023) {{
                    Serial.println("Error: usage - mod [id] [value]");
                }} else {{
                    motors[indexNum].drive(value);
                    Serial.println("ok");
                }}
            }} else {{
                Serial.println("Error: usage - mod [id] [value]");
            }}
        }} else {{
            Serial.println("Error: usage - mod [id] [value]");
        }}
    }}
    else if(args[0].equals(String("mos"))){{ // motor stop
        if(numArgs == 2) {{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}) {{
                motors[indexNum].stop();
                Serial.println("ok");
            }} else {{
                Serial.println("Error: usage - mos [id]");
            }}
        }} else {{
            Serial.println("Error: usage - mos [id]");
        }}
    }}
'''.format(length)

    def get_indices(self):
        for i, motor in enumerate(self.motorList):
            yield i, motor
