from appendages.component_list import ComponentList


class Encoder:
    def __init__(self, label, pinA, pinB):
        self.label = label
        self.pinA = pinA
        self.pinB = pinB


class EncoderList(ComponentList):
    TIER = 1

    def __init__(self):
        self.encoderDict = {}
        self.encoderList = []

    def add(self, json_item):
        encoder = Encoder(json_item['label'], json_item['pinA'], json_item['pinB'])
        self.encoderDict[json_item['label']] = encoder
        self.encoderList.append(encoder)
        self.encoderList.sort(key=lambda x: x.label, reverse=False)

    def get(self, label):
        if label in self.encoderDict:
            return self.encoderDict[label]
        else:
            return None

    def get_includes(self):
        return '#include "Encoder.h"\n'

    def get_pins(self):
        rv = ""
        for encoder in self.encoderList:
            rv += "const char {0:s}_pinA = {1:d};\n".format(encoder.label, encoder.pinA)
            rv += "const char {0:s}_pinB = {1:d};\n".format(encoder.label, encoder.pinB)
        return rv

    def get_constructor(self):
        rv = ""
        for i, encoder in enumerate(self.encoderList):
            rv += "const char {0:s}_index = {1:d};\n".format(encoder.label, i)
        rv += "Encoder encoders[{0:d}] = {{\n".format(len(self.encoderList))
        for encoder in self.encoderList:
            rv += "\tEncoder({0:s}_pinA, {0:s}_pinB),\n".format(encoder.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        rv = ""
        for encoder in self.encoderList:
            rv += "\tpinMode({0:s}_pinA, INPUT);\n".format(encoder.label)
            rv += "\tpinMode({0:s}_pinB, INPUT);\n".format(encoder.label)
        return rv

    def get_response_block(self):
        length = len(self.encoderList)
        return '''\t\telse if(args[0].equals(String("re"))){{ // read encoders
        if(numArgs == 2){{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}){{
                Serial.println(encoders[indexNum].read());
            }} else {{
                Serial.println("Error: usage - re [id]");
            }}
        }} else {{
            Serial.println("Error: usage - re [id]");
        }}
    }}
    else if(args[0].equals(String("ze"))){{ // zero encoders
        if(numArgs == 2){{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}){{
                encoders[indexNum].write(0);
                Serial.println("ok");
            }} else {{
                Serial.println("Error: usage - ze [id]");
            }}
        }} else {{
            Serial.println("Error: usage - ze [id]");
        }}
    }}
'''.format(length)

    def get_indices(self):
        for i, encoder in enumerate(self.encoderList):
            yield i, encoder
