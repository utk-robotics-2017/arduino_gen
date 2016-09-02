class Encoder:
    def __init__(self, label, pinA, pinB):
        self.label = label
        self.pinA = pinA
        self.pinB = pinB


class encoderList:
    def __init__(self):
        self.tier = 1
        self.encoderDict = {}
        self.encoderList = []

    def add(self, json_item):
        encoder = Encoder(json_item['label'], json_item['pinA'], json_item['pinB'])
        self.encoderDict[json_item['label']] = encoder
        self.encoderList.append(encoder)
        self.encoderList.sort(key=lambda x: x.label, reverse=False)

    def get(self, label):
        return self.encoderDict['label']

    def get_includes(self):
        return '#include "Encoder.h"\n'

    def get_pins(self):
        rv = ""
        for encoder in self.encoderList:
            rv += "const char %s_pinA = %d;\n" % (encoder.label, encoder.pinA)
            rv += "const char %s_pinB = %d;\n" % (encoder.label, encoder.pinB)
        return rv

    def get_constructor(self):
        rv = ""
        for i, encoder in enumerate(self.encoderList):
            rv += "const char %s_index = %d;\n" % (encoder.label, i)
        rv += "Encoder encoders[%d] = {\n" % len(self.encoderList)

        for encoder in self.encoderList:
            rv += "    Encoder(%s_pinA, %s_pinB),\n" % (encoder.label, encoder.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        rv = ""
        for encoder in self.encoderList:
            rv += "    pinMode(%s_pinA, INPUT);\n" % encoder.label
            rv += "    pinMode(%s_pinB, INPUT);\n" % encoder.label
        return rv

    def get_loop_functions(self):
        return ""

    def get_response_block(self):
        length = len(self.encoderList)
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

    def get_indices(self):
        for i, encoder in enumerate(self.encoderList):
            yield i, encoder
