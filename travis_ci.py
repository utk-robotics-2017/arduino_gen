import os
from ArduinoGen import ArduinoGen
deviceJsonFile = "travis_ci.json"
ag = ArduinoGen(arduino="travis_ci")
ag.setParentFolder(os.path.dirname(os.path.realpath(__file__)))
ag.setupFolder()
ag.readConfig(deviceJsonFile)
ag.generateOutput()
