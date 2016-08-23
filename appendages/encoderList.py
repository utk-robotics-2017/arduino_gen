class encoder:
    def __init__(self, label, pinA, pinB):
        self.label = label
        self.pinA = pinA
        self.pinB = pinB


class encoderList:
    def __init__(self):
        self.sensors = dict()

    def add(self, json_item):
        self.sensors[json_item['label']] = encoder(json_item['label'], json_item['pinA'], json_item['pinB'])

    def get(self, label):
        return self.sensors['label']

    def get_include(self):
        return "#include \"Encoder.h\""

    def get_include_files(self):
        return []

    def get_pins(self):
        rv = ""
        for sensor in self.sensors.values():
            rv = rv + "const char %s_pinA = %d;\n" % (sensor.label, sensor.pinA)
            rv = rv + "const char %s_pinB = %d;\n" % (sensor.label, sensor.pinB)
        return rv

    def get_constructor(self):
        rv = ""
        for i, label in zip(range(len(self.sensors)), self.sensors.keys()):
            rv = rv + "const char %s_index = %d;\n" % (label, i)
        rv = rv + "Encoder encoders[%d] = {\n" % len(self.sensors)

        for label in self.sensors.keys():
            rv = rv + "    Encoder(%s_pinA, %s_pinB),\n" % (label, label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        return ""

    def get_loop_functions(self):
        return ""

    def get_response_block(self):
        length = len(self.sensors)
        return '''    else if(args[0].equals(String("re"))){ // read encoders
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                Serial.println(encoders[indexNum].read());
            } else {
                Serial.println("Error: usage - re [id]");
            }
        } else {
            Serial.println("Error: usage - re [id]");
        }
    }
    else if(args[0].equals(String("ze"))){ // zero encoders
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                encoders[indexNum].write(0);
                Serial.println("ok");
            } else {
                Serial.println("Error: usage - ze [id]");
            }
        } else {
            Serial.println("Error: usage - ze [id]");
        }
    }
''' % (length, length)

    def get_extra_functions(self):
        return ""
