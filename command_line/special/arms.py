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

    def get_constructor(self):
        rv = ""
        for i in range(len(self.arm_list)):
            rv = rv + "const char %s_base_index = %d;\n" % (self.arm_list[i].label, i * 5)
            rv = rv + "const char %s_shoulder_index = %d;\n" % (self.arm_list[i].label, i * 5 + 1)
            rv = rv + "const char %s_elbow_index = %d;\n" % (self.arm_list[i].label, i * 5 + 2)
            rv = rv + "const char %s_wrist_index = %d;\n" % (self.arm_list[i].label, i * 5 + 3)
            rv = rv + "const char %s_wrist_rotate_index = %d;\n" % (self.arm_list[i].label, i * 5 + 4)
        rv = rv + ("Servo arm_servos[%d];\n") % (len(self.arm_list)*5)
        return rv

    def get_setup(self):
        rv = ""
        for arm in self.arm_list:
            rv = rv + "    arm_servos[%s_base_index].attach(%s_base_pin);\n" % (arm.label, arm.label)
            rv = rv + "    arm_servos[%s_shoulder_index].attach(%s_shoulder_pin);\n" % (arm.label, arm.label)
            rv = rv + "    arm_servos[%s_elbow_index].attach(%s_elbow_pin);\n" % (arm.label, arm.label)
            rv = rv + "    arm_servos[%s_wrist_index].attach(%s_wrist_pin);\n" % (arm.label, arm.label)
            rv = rv + "    arm_servos[%s_wrist_rotate_index].attach(%s_wrist_rotate_pin);\n" % (arm.label, arm.label)
        rv = rv + "\n"
        return rv

    def get_response_block(self):
        rv = '''    else if(args[0].equals(String("sa"))) { // set arm
        if(numArgs == 7) {
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                int posbase = args[2].toInt();
                int posshoulder = args[3].toInt();
                int poselbow = args[4].toInt();
                int poswrist = args[5].toInt();
                int poswristrotate = args[6].toInt();
                if (!arm_servos[indexNum * 5].attached()) {
                    arm_servos[indexNum * 5].attach(3);
                    arm_servos[indexNum * 5 + 1].attach(5);
                    arm_servos[indexNum * 5 + 2].attach(6);
                    arm_servos[indexNum * 5 + 3].attach(9);
                    arm_servos[indexNum * 5 + 4].attach(11);
                }
                arm_servos[indexNum * 5].write(posbase);
                arm_servos[indexNum * 5 + 1].write(posshoulder);
                arm_servos[indexNum * 5 + 2].write(poselbow);
                arm_servos[indexNum * 5 + 3].write(poswrist);
                arm_servos[indexNum * 5 + 4].write(poswristrotate);
                Serial.println("ok");
            } else {
                Serial.println("error: usage - 'sa [id] [base] [shoulder] [elbow] [wrist] [wristrotate]'");
            }
        } else {
            Serial.println("error: usage - 'sa [id] [base] [shoulder] [elbow] [wrist] [wristrotate]'");
        }
    }
    else if(args[0].equals(String("das"))) { // detach arm servos
        if(numArgs == 2) {
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                arm_servos[indexNum * 5].detach();
                arm_servos[indexNum * 5 + 1].detach();
                arm_servos[indexNum * 5 + 2].detach();
                arm_servos[indexNum * 5 + 3].detach();
                arm_servos[indexNum * 5 + 4].detach();
                Serial.println("ok");
            } else {
                Serial.println("error: usage - 'ds [id]'");
            }
        } else {
            Serial.println("error: usage - 'ds [id]'");
        }
    }
''' % (len(self.arm_list), len(self.arm_list))
        return rv
