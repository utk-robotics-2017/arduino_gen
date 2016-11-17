from appendages.electronic_component_detector_list import ComponentList


class ElectronicComponentDetector:
    #List Pinouts
    def __init__(self, label):
        self.label = label



class ElectronicComponentDetectorList(ComponentList):
    TIER = 1

    def __init__(self):
        self.electronic_component_detectorList = []

    def add(self, json_item):
        self.electronic_component_detector_list.append(Electronic_Component_Detector(json_item['label']))

    def get_includes(self):
        return '#include "ElectronicComponentDetector.h"\n'

    def get_constructor(self):
        #Leave blank for now (Only 1 Stage 1)
        rv = ""
        rv += "ElectronicComponentDetector ecds[{0:d}] = {{\n".format(len(self.electronic_component_detectorList))
        for electronic_component_detector in self.electronic_component_detectorList:
            rv += "\tElectronicComponentDetector(),\n"
        rv = rv[:-2] + "\n};\n"    
        #Creates object from the .CPP & .H
        return rv

    def get_setup(self):
        rv = ""
        rv += "for(int i = 0 ; i < {0:d} ; i++) {{ \n".format(len(self.electronic_component_detectorList))
        for electronic_component_detector in self.electronic_component_detectorList:
            rv += "ecds[i].init();\n"
        rv += "}\n"
        return rv
        
        
    def get_commands(self):
        #List of serial commands
        return "\tkDecode\n,\tkDecodeResult\n"

    def get_command_attaches(self):
        rv = "\tcmdMessenger.attach(kDecode, Decode);\n"
        return rv
    
    def get_command_functions(self):
        rv = "void Decode() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.electronic_component_detectorList))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kDecode);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tchar pad = cmdMessenger.readBinArg<char>();\n"
        rv += "\tchar debug = cmdMessenger.readBinArg<char>();\n"
        rv += "\tchar Code[5];\n"
        rv += "\tecds[indexNum].decode(pad, Code, debug);\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kDecode);\n"
        rv += "\tcmdMessenger.sendStartCmd(kDecodeResult);\n"
        rv += "\tfor(int x = 0 ; x <= 4 ; x++ ) { \n"
        rv += "\t\tcmdMessenger.sendBinArg(Code[x]);\n"
        rv += "\t}\n"
        rv += "}\n\n"
        return rv

    def get_core_values(self):
        for i, arm in enumerate(self.electronic_component_detectorList):
            config = {}
            config['index'] = i
            config['type'] = "ElectronicComponentDetector"
            config['label'] = arm.label
            yield config
