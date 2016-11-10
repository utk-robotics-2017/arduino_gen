from appendages.component_list import ComponentList


class LCD_display:
    def __init__(self,label,pin)
        self.label = label
        self.pin = pin


class LcdDisplayList(ComponentList):

    TIER = 1

    def __init__(self):
        self.digital_sensor_list = []
        self.analog_sensor_list = []

    def add(self, json_item):
        if(json_item['digital']):
            self.digital_sensor_list.append(LineSensor(json_item['label'], json_item['pin']))
        else:
            self.analog_sensor_list.append(LineSensor(json_item['label'], json_item['pin']))
    def get_pins():
    def get_includes
    def get_commands(self):
        rv = ""
        if(len(self.digital_sensor_list) > 0)
            rv +=
        if(len(self.digital_sensor_list) > 0)
