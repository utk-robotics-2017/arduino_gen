import os
from ArduinoGen import ArduinoGen
confFolder = "./conf"
confFolderAbsPath = os.path.abspath(confFolder)
deviceJsonFile = confFolderAbsPath + "/mega.json"
ag = ArduinoGen(arduino="mega", arduinoType="mega2560")
ag.setParentFolder(os.path.dirname(os.path.realpath(__file__)))
ag.setupFolder()
ag.readConfig(deviceJsonFile)
ag.generateOutput()
