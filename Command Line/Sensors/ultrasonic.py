class ultrasonic:
    def __init__(self, id, pin):
        self.id = id
        self.pin = pin

    def get_sensor_name(self):
        return "ultrasonic"

    def get_include(self):
        return "NewPing.h"

    def get_pins(self):
        return "char ultrasonic%d_pin = %d" % (self.id, self.pin)

    def get_constructor(self):
        return ("NewPing ultrasonic%d = new NewPing(ultrasonic%d_pin, ultrasonic%d_pin);") % (self.id, self.id, self.id)

    def get_command(self):
        return "rus"

    def get_response(self):
        return ("unsigned int response = ultrasonic%d.ping();\nSerial.println(response);") % (self.id)
