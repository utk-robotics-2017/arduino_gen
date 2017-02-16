from appendages.component_list import ComponentList


class Encoder:
    def __init__(self, label, pin_a, pin_b, ticks_per_rev):
        self.label = label
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.ticks_per_rev = ticks_per_rev


class EncoderList(ComponentList):
    TIER = 1

    def __init__(self):
        self.list_ = []

    def add(self, json_item, device_dict, device_type):
        encoder = Encoder(json_item['label'], json_item['pin_a'], json_item['pin_b'], json_item['ticks_per_rev'])
        self.list_.append(encoder)
        return encoder

    def get_includes(self):
        return '#include "Encoder.h"\n'

    def get_pins(self):
        rv = ""
        for encoder in self.list_:
            rv += "const char {0:s}_pin_a = {1:d};\n".format(encoder.label, encoder.pin_a)
            rv += "const char {0:s}_pin_b = {1:d};\n".format(encoder.label, encoder.pin_b)
        rv += "\n"
        return rv

    def get_constructors(self):
        rv = ""
        for i, encoder in enumerate(self.list_):
            rv += "const char {0:s}_index = {1:d};\n".format(encoder.label, i)
        rv += "Encoder encoders[{0:d}] = {{\n".format(len(self.list_))
        for encoder in self.list_:
            rv += "\tEncoder({0:s}_pin_a, {0:s}_pin_b),\n".format(encoder.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        rv = ""
        for encoder in self.list_:
            rv += "\tpinMode({0:s}_pin_a, INPUT);\n".format(encoder.label)
            rv += "\tpinMode({0:s}_pin_b, INPUT);\n".format(encoder.label)
        return rv

    def get_commands(self):
        return "\tkReadEncoder,\n\tkReadEncoderResult,\n\tkZeroEncoder,\n"

    def get_command_attaches(self):
        rv = "\tcmdMessenger.attach(kReadEncoder, readEncoder);\n"
        rv += "\tcmdMessenger.attach(kZeroEncoder, zeroEncoder);\n"
        return rv

    def get_command_functions(self):
        rv = "void readEncoder() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.list_))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kReadEncoder);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kReadEncoder);\n"
        rv += "\tcmdMessenger.sendBinCmd(kReadEncoderResult, encoders[indexNum].read());\n"
        rv += "}\n\n"

        rv += "void zeroEncoder() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.list_))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kZeroEncoder);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tencoders[indexNum].write(0);\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kZeroEncoder);\n"
        rv += "}\n\n"
        return rv

    def get_indices(self):
        for i, encoder in enumerate(self.list_):
            yield i, encoder

    def get_core_values(self):
        for i, encoder in enumerate(self.list_):
            a = {}
            a['index'] = i
            a['label'] = encoder.label
            a['type'] = "Encoder"
            a['ticks_per_rev'] = encoder.ticks_per_rev
            yield a
