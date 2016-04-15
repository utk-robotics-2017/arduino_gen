class servo:
    def __init__(self, label, pin):
        self.label = label
        self.pin = pin


class servos:
    def __init__(self):
        self.actuator_list = []

    def add_actuator(self, label, pin):
        self.actuator_list.append(servo(label, pin))