import os
from ArduinoGen import ArduinoGen
confFolder = "./conf"
confFolderAbsPath = os.path.abspath(confFolder)
deviceJsonFile = confFolderAbsPath + "/travis_ci.json"
ag = ArduinoGen(arduino="travis_ci")
ag.setParentFolder(os.path.dirname(os.path.realpath(__file__)))
ag.setupFolder()
ag.readConfig(deviceJsonFile)
ag.generateOutput()
