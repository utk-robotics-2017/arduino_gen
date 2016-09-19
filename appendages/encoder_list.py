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
        rv += "\n"
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

    def get_commands(self):
        return "\tkReadEncoder,\n\tkReadEncoderResult,\n\tkZeroEncoder,\n"

    def get_command_attaches(self):
        rv = "\tcmdMessenger.attach(kReadEncoder, readEncoder);\n"
        rv += "\tcmdMessenger.attach(kZeroEncoder, zeroEncoder);\n"
        return rv

    def get_command_functions(self):
        rv = "void readEncoder() {\n"
        rv += "\tif(cmdMessenger.available()) {\n"
        rv += "\t\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\t\tif(indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.encoderList))
        rv += "\t\t\tcmdMessenger.sendBinCmd(kError, kReadEncoder);\n"
        rv += "\t\t\treturn;\n"
        rv += "\t\t}\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kAcknowledge, kReadEncoder);\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kReadEncoderResult, encoders[indexNum].read());\n"
        rv += "\t} else {\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kReadEncoder);\n"
        rv += "\t}\n"
        rv += "}\n\n"

        rv += "void zeroEncoder() {\n"
        rv += "\tif(cmdMessenger.available()) {\n"
        rv += "\t\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\t\tif(indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.encoderList))
        rv += "\t\t\tcmdMessenger.sendBinCmd(kError, kZeroEncoder);\n"
        rv += "\t\t\treturn;\n"
        rv += "\t\t}\n"
        rv += "\t\tencoders[indexNum].write(0);\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kAcknowledge, kZeroEncoder);\n"
        rv += "\t} else {\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kZeroEncoder);\n"
        rv += "\t}\n"
        rv += "}\n\n"
        return rv

    def get_indices(self):
        for i, encoder in enumerate(self.encoderList):
            yield i, encoder

    def get_core_values(self):
        for i, encoder in enumerate(self.encoderList):
            a = {}
            a['index'] = i
            a['label'] = encoder.label
            a['type'] = "Encoder"
            yield a
