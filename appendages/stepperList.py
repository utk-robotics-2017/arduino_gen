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
        self.actuators = []

    def add(self, json_item):
        self.actuators[json_item['label']] = Stepper(json_item['label'], json_item['num_steps'], json_item['pinA'], json_item['pinB'], json_item['pinC'], json_item['pinD'], json_item['initial_speed'])


    def get(self, label):
        return self.actuators[label]

    def get_include(self):
        return "#include \"Stepper.h\";"

    def get_include_files(self):
        return ""

    def get_pins(self):
        rv = ""
        for actuator in self.actuators.values():
            rv += "const char %s_pinA = %d;\n" % (actuator.label, actuator.pinA)
            rv += "const char %s_pinB = %d;\n" % (actuator.label, actuator.pinB)
            rv += "const char %s_pinC = %d;\n" % (actuator.label, actuator.pinC)
            rv += "const char %s_pinD = %d;\n" % (actuator.label, actuator.pinD)
        return rv

    def get_constructor(self):
        rv = ""
        for i, label in zip(range(len(self.actuators)), self.actuators.keys()):
            rv += "const char %s_index = %d;\n" % (label, i)

        rv += ("Stepper steppers[%d] = {\n") % (len(self.actuators))
        for stepper in self.actuators:
            rv += "    Stepper(%d, %s_pinA, %s_pinB, %s_pinC, %_pinD)," % (stepper.steps, stepper.label, stepper.label, stepper.label, stepper.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        rv = ""
        for stepper in self.actuators:
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
''' % (len(self.actuators), len(self.actuators))

def get_extra_functions(self):
    return ""
