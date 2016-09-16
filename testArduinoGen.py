import os
from ArduinoGen import ArduinoGen
confFolder = "./conf"
confFolderAbsPath = os.path.abspath(confFolder)
# deviceJsonFile = confFolderAbsPath + "/template.json"
# ag = ArduinoGen(arduino="template")
deviceJsonFile = confFolderAbsPath + "/mega.json"
ag = ArduinoGen(arduino="mega")
ag.setParentFolder(os.path.dirname(os.path.realpath(__file__)))
ag.setupFolder()
ag.readConfig(deviceJsonFile)
ag.generateOutput()
ag.upload()
