from appendages.component_list import ComponentList


class LCD_display:
    def __init__(self,label,pin)
        self.label = label
        self.pin = pin


class LcdDisplayList(ComponentList):

    TIER = 1

    def __init__(self):
        self.digital_lcd_list = []
        self.analog_lcd_list = []

    def add(self, json_item):
        if(json_item['digital']):
            self.digital_sensor_list.append(LineSensor(json_item['label'], json_item['pin']))
        else:
            self.analog_sensor_list.append(LineSensor(json_item['label'], json_item['pin']))
    def get_pins(self):
        rv = ""
        for lcd16 in self.digital_lcd_list:
            rv += "const char {0:s}_pin = {1:d};\n".format(sensor.label, sensor.pin)
        for lcd16 in self.analog_lcd_list:
            rv += "const char {0:s}_pin = {1:d};\n".format(sensor.label, sensor.pin)
        rv += "\n"

    def get_includes(self):
        return '#include "lcd16.h"\n'

    def get_commands(self):
        rv = ""
        if(len(self.digital_sensor_list) > 0)
            rv +=
        if(len(self.digital_sensor_list) > 0)
            rv +=
        return rv
    def get_constructor(self):
    def get_setup(self):
    def get_command_attaches():
    def get_command_functions():
    def get_core_values():
