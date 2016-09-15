class Stepper:
    def __init__(self, label, steps, pinA, pinB, pinC, pinD, initial_speed):
        self.label = label
        self.steps = steps
        self.pinA = pinA
        self.pinB = pinB
        self.pinC = pinC
        self.pinD = pinD
        self.initial_speed = initial_speed


class StepperList:
    TIER = 1

    def __init__(self):
        self.stepperDict = {}
        self.stepperList = []

    def add(self, json_item):
        stepper = Stepper(json_item['label'], json_item['steps'],
                          json_item['pinA'], json_item['pinB'],
                          json_item['pinC'], json_item['pinD'],
                          json_item['initial_speed'])
        self.stepperDict[json_item['label']] = stepper
        self.stepperList.append(stepper)
        self.stepperList.sort(key=lambda x: x.label, reverse=False)

    def get(self, label):
        return self.actuators[label]

    def get_includes(self):
        return "#include \"Stepper.h\""

    def get_pins(self):
        rv = ""
        for stepper in self.stepperList:
            rv += "const char {0:s}_pinA = {1:d};\n".format(stepper.label, stepper.pinA)
            rv += "const char {0:s}_pinB = {1:d};\n".format(stepper.label, stepper.pinB)
            rv += "const char {0:s}_pinC = {1:d};\n".format(stepper.label, stepper.pinC)
            rv += "const char {0:s}_pinD = {1:d};\n".format(stepper.label, stepper.pinD)
        return rv

    def get_constructor(self):
        rv = ""
        for i, stepper in enumerate(self.stepperList):
            rv += "const char {0:s}_index = {1:d};\n".format(stepper.label, i)

        rv += ("Stepper steppers[{0:d}] = {{\n").format(len(self.stepperList))
        for stepper in self.stepperList:
            rv += ("\tStepper({0:d}, {1:s}_pinA, {1:s}_pinB, {1:s}_pinC, {1:s}_pinD),")\
                    .format(stepper.steps, stepper.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        rv = ""
        for stepper in self.stepperList:
            rv += "\tpinMode({0:s}_pinA, OUTPUT);\n".format(stepper.label)
            rv += "\tpinMode({0:s}_pinB, OUTPUT);\n".format(stepper.label)
            rv += "\tpinMode({0:s}_pinC, OUTPUT);\n".format(stepper.label)
            rv += "\tpinMode({0:s}_pinD, OUTPUT);\n".format(stepper.label)

        for stepper in self.stepperList:
            rv += ("\tsteppers[{0:s}_index].setSpeed({1:f});\n").format(stepper.label,
                                                                        stepper.initial_speed)
        rv += "\n"

        return rv

    def get_loop_functions(self):
        return ""

    def get_response_block(self):
        return '''\t\telse if(args[0].equals(String("sssp"))){{ // set stepper speed
    if(numArgs == 3){{
        int indexNum = args[1].toInt();
        if(indexNum > -1 && indexNum < {0:d}){{
            int value = args[2].toInt();
            steppers[indexNum].setSpeed(balue);
            Serial.println("ok");
        }} else {{
            Serial.println("Error: usage - sssp [id] [value]");
        }}
    }} else {{
        Serial.println("Error: usage - sssp [id] [value]");
    }}
}}
else if(args[0].equals(String("sss"))){{ // step stepper
    if(numArgs == 3){{
        int indexNum = args[1].toInt();
        if(indexNum > -1 && indexNum < {0:d}){{
            int value = args[2].toInt();
            stepper[indexNum].step(value);
            Serial.println("ok");
        }} else {{
            Serial.println("Error: usage - sss [id] [value]");
        }}
    }} else {{
        Serial.println("Error: usage - sss [id] [value]");
    }}
}}
'''.format(len(self.stepperList))

    def get_extra_functions(self):
        return ""

    def get_indices(self):
        for i, stepper in enumerate(self.stepperList):
            yield i, stepper
