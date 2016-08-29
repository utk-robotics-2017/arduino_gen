class arm:
    def __init__(self, label, base, shoulder, elbow, wrist, wrist_rotate):
        self.label = label
        self.base = base
        self.shoulder = shoulder
        self.elbow = elbow
        self.wrist = wrist
        self.wrist_rotate = wrist_rotate


class armList:
    def __init__(self):
        self.tier = 2
        self.arm_list = []

    def add(self, json_item, servos):

        base_servo = servos.get(json_item['base_label'])
        shoulder_servo = servos.get(json_item['shoulder_label'])
        elbow_servo = servos.get(json_item['elbow_label'])
        wrist_servo = servos.get(json_item['wrist_label'])
        wrist_rotate_servo = servos.get(json_item['wrist_rotate_label'])

        self.arm_list.append(arm(json_item['label'], base_servo, shoulder_servo, elbow_servo, wrist_servo, wrist_rotate_servo))

    def get_include(self):
        return "#include \"Arm.h\";"

    def get_include_files(self):
        return ['Arm.h', 'Arm.cpp']

    def get_pins(self):
        return ""

    def get_constructor(self):
        rv = "Arm arms[%d] = {\n" % len(self.arm_list)
        for arm in self.arm_list:
            rv += "    Arm(%s_index, %s_index, %s_index, %s_index, %s_index, servo_pins, servos),\n" % (arm.base.label, arm.shoulder.label, arm.elbow.label, arm.wrist.label, arm.wrist_rotate.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        return ""

    def get_response_block(self):
        return '''    else if(args[0].equals(String("sa"))) { // set arm
        if(numArgs == 7) {
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                int posbase = args[2].toInt();
                int posshoulder = args[3].toInt();
                int poselbow = args[4].toInt();
                int poswrist = args[5].toInt();
                int poswristrotate = args[6].toInt();

                arms[indexNum].set(posbase, posshoulder, poselbow, poswrist, poswristrotate);
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
                arms[indexNum].detach();
                Serial.println("ok");
            } else {
                Serial.println("error: usage - 'ds [id]'");
            }
        } else {
            Serial.println("error: usage - 'ds [id]'");
        }
    }
''' % (len(self.arm_list), len(self.arm_list))

    def get_extra_functions(self):
        return ""
