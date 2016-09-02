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
            rv += "const char %s_pinA = %d;\n" % (stepper.label, stepper.pinA)
            rv += "const char %s_pinB = %d;\n" % (stepper.label, stepper.pinB)
            rv += "const char %s_pinC = %d;\n" % (stepper.label, stepper.pinC)
            rv += "const char %s_pinD = %d;\n" % (stepper.label, stepper.pinD)
        return rv

    def get_constructor(self):
        rv = ""
        for i, stepper in enumerate(self.stepperList):
            rv += "const char %s_index = %d;\n" % (stepper.label, i)

        rv += ("Stepper steppers[%d] = {\n") % (len(self.stepperList))
        for stepper in self.stepperList:
            rv += "    Stepper(%d, %s_pinA, %s_pinB, %s_pinC, %_pinD)," % (stepper.steps, stepper.label, stepper.label, stepper.label, stepper.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        rv = ""
        for stepper in self.stepperList:
            rv += "    pinMode(%s_pinA, OUTPUT);\n" % stepper.label
            rv += "    pinMode(%s_pinB, OUTPUT);\n" % stepper.label
            rv += "    pinMode(%s_pinC, OUTPUT);\n" % stepper.label
            rv += "    pinMode(%s_pinD, OUTPUT);\n" % stepper.label

        for stepper in self.stepperList:
            rv += "    steppers[%s_index].setSpeed(%s_pin);\n" % (stepper.label, stepper.initial_speed)
        rv += "\n"

        return rv
    def get_loop_functions(self):
        return ""

    def get_response_block(self):
        return '''    else if(args[0].equals(String("sssp"))){ // set stepper speed
    if(numArgs == 3){
        int indexNum = args[1].toInt();
        if(indexNum > -1 && indexNum < %d){
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
        if(indexNum > -1 && indexNum < %d){
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
''' % (len(self.stepperList), len(self.stepperList))

    def get_extra_functions(self):
        return ""

    def get_indices(self):
        for i, stepper in enumerate(self.stepperList):
            yield i, stepper
