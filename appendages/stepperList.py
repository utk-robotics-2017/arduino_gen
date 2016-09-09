class Stepper:
    def ___init__(self, label, steps, pinA, pinB, pinC, pinD, initial_speed):
        self.label = label
        self.steps = steps
        self.pinA = pinA
        self.pinB = pinB
        self.pinC = pinC
        self.pinD = pinD
        self.initial_speed = initial_speed

class stepperList:
    def __init__(self):
        self.tier = 1
        self.stepperDict = {}
        self.stepperList = []

    def add(self, json_item):
        stepper = Stepper(json_item['label'], json_item['num_steps'], json_item['pinA'], json_item['pinB'], json_item['pinC'], json_item['pinD'], json_item['initial_speed'])
        self.stepperDict[json_item['label']] = stepper
        self.stepperList.append(stepper)
        self.stepperList.sort(key=lambda x: x.label, reverse=False)

    def get(self, label):
        return self.actuators[label]

    def get_include(self):
        return "#include \"Stepper.h\""

    def get_pins(self):
        rv = ""
        for stepper in self.stepperList:
            rv += "const char {}_pinA = %d;\n".format(stepper.label, stepper.pinA)
            rv += "const char {}_pinB = %d;\n".format(stepper.label, stepper.pinB)
            rv += "const char {}_pinC = %d;\n".format(stepper.label, stepper.pinC)
            rv += "const char {}_pinD = %d;\n".format(stepper.label, stepper.pinD)
        return rv

    def get_constructor(self):
        rv = ""
        for i, stepper in enumerate(self.stepperList):
            rv += "const char {}_index = %d;\n".format(stepper.label, i)

        rv += ("Stepper steppers[{}] = {\n").format(len(self.stepperList))
        for stepper in self.stepperList:
            rv += "    Stepper({}, {}_pinA, {}_pinB, {}_pinC, {}_pinD),".format(stepper.steps, stepper.label, stepper.label, stepper.label, stepper.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        rv = ""
        for stepper in self.stepperList:
            rv += "    pinMode({}_pinA, OUTPUT);\n".format(stepper.label)
            rv += "    pinMode({}_pinB, OUTPUT);\n".format(stepper.label)
            rv += "    pinMode({}_pinC, OUTPUT);\n".format(stepper.label)
            rv += "    pinMode({}_pinD, OUTPUT);\n".format(stepper.label)

        for stepper in self.stepperList:
            rv += "    steppers[{}_index].setSpeed({}_pin);\n".format(stepper.label, stepper.initial_speed)
        rv += "\n"

        return rv
    def get_loop_functions(self):
        return ""

    def get_response_block(self):
        return '''    else if(args[0].equals(String("sssp"))){ // set stepper speed
    if(numArgs == 3){
        int indexNum = args[1].toInt();
        if(indexNum > -1 && indexNum < {}){
            int value = args[2].toInt();
            steppers[indexNum].setSpeed(balue);
            Serial.println("ok");
        } else {
            Serial.println("Error: usage - sssp [id] [value]");
        }
    } else {
        Serial.println("Error: usage - sssp [id] [value]");
    }
}
else if(args[0].equals(String("sss"))){ // step stepper
    if(numArgs == 3){
        int indexNum = args[1].toInt();
        if(indexNum > -1 && indexNum < {}){
            int value = args[2].toInt();
            stepper[indexNum].step(value);
            Serial.println("ok");
        } else {
            Serial.println("Error: usage - sss [id] [value]");
        }
    } else {
        Serial.println("Error: usage - sss [id] [value]");
    }
}
'''.format(len(self.stepperList), len(self.stepperList))

    def get_extra_functions(self):
        return ""

    def get_indices(self):
        for i, stepper in enumerate(self.stepperList):
            yield i, stepper
