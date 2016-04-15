class arm:
    def __init__(self, label, base_pin, shoulder_pin, elbow_pin, wrist_pin, wrist_rotate_pin):
        self.label = label
        self.base_pin = base_pin
        self.shoulder_pin = shoulder_pin
        self.elbow_pin = elbow_pin
        self.wrist_pin = wrist_pin
        self.wrist_rotate_pin = wrist_rotate_pin


class arms:
    def __init__(self):
        self.arm_list = []

    def add(self, label, base_pin, shoulder_pin, elbow_pin, wrist_pin, wrist_rotate_pin):
        self.arm_list.append(arm(label, base_pin, shoulder_pin, elbow_pin, wrist_pin, wrist_rotate_pin))

    def get_include(self):
        return "#include \"Servo.h\";"

    def get_pins(self):
        rv = ""
        for arm in self.arm_list:
            rv = rv + "const char %s_base_pin = %d;\n" % (arm.label, arm.base_pin)
            rv = rv + "const char %s_shoulder_pin = %d;\n" % (arm.label, arm.shoulder_pin)
            rv = rv + "const char %s_elbow_pin = %d;\n" % (arm.label, arm.elbow_pin)
            rv = rv + "const char %s_wrist_pin = %d;\n" % (arm.label, arm.wrist_pin)
            rv = rv + "const char %s_wrist_rotate_pin = %d;\n" % (arm.label, arm.wrist_rotate_pin)

        return rv
