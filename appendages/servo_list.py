from appendages.component_list import ComponentList


class Servo:
    def __init__(self, label, pin):
        self.label = label
        self.pin = pin


class ServoList(ComponentList):
    TIER = 1

    def __init__(self):
        self.servoDict = {}
        self.servoList = []

    def add(self, json_item):
        servo = Servo(json_item['label'], json_item['pin'])
        self.servoDict[servo.label] = servo
        self.servoList.append(servo)
        self.servoList.sort(key=lambda x: x.label, reverse=False)

    def get(self, label):
        if label in self.servoDict:
            return self.servoDict[label]
        else:
            return None

    def get_includes(self):
        return "#include \"Servo.h\""

    def get_pins(self):
        rv = ""
        for actuator in self.servoList:
            rv += "const char {0:s}_pin = {1:d};\n".format(actuator.label, actuator.pin)
        return rv

    def get_constructor(self):
        rv = ""
        for i, servo in enumerate(self.servoList):
            rv += "const char {0:s}_index = {1:d};\n".format(servo.label, i)

        rv += "char servo_pins[{0:d}] = {{\n".format(len(self.servoList))
        for servo in self.servoList:
            rv += ("\t{0:s}_pin,\n").format(servo.label)
        rv = rv[:-2] + "\n};\n"

        rv += ("Servo servos[{0:d}];\n").format(len(self.servoList))
        return rv

    def get_setup(self):
        rv = ""
        for servo in self.servoList:
            rv += "\tservos[{0:s}_index].attach({0:s}_pin);\n".format(servo.label)
        rv += "\n"

        return rv

    def get_response_block(self):
        return '''\t\telse if(args[0].equals(String("ss"))){{ // set servo
        if(numArgs == 3){{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}){{
                int value = args[2].toInt();
                if(!servos[indexNum].attached()){{
                    servos[indexNum].attach(servo_pins[indexNum]);
                }}
                servos[indexNum].write(value);
                Serial.println("ok");
            }} else {{
                Serial.println("Error: usage - ss [id] [value]");
            }}
        }} else {{
            Serial.println("Error: usage - ss [id] [value]");
        }}
    }}
    else if(args[0].equals(String("sd"))){{ // detach servo
        if(numArgs == 2){{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}){{
                servos[indexNum].detach();
                Serial.println("ok");
            }} else {{
                Serial.println("Error: usage - sd [id]");
            }}
        }} else {{
            Serial.println("Error: usage - sd [id]");
        }}
    }}
'''.format(len(self.servoList))

    def get_indices(self):
        for i, servo in enumerate(self.servoList):
            yield i, servo
