from appendages.component_list import ComponentList


class Arm:
    def __init__(self, label, base, shoulder, elbow, wrist, wrist_rotate):
        self.label = label
        self.base = base
        self.shoulder = shoulder
        self.elbow = elbow
        self.wrist = wrist
        self.wrist_rotate = wrist_rotate


class ArmList(ComponentList):
    TIER = 2

    def __init__(self):
        self.arm_list = []

    def add(self, json_item, servos):

        base_servo = servos.get(json_item['base_label'])
        shoulder_servo = servos.get(json_item['shoulder_label'])
        elbow_servo = servos.get(json_item['elbow_label'])
        wrist_servo = servos.get(json_item['wrist_label'])
        wrist_rotate_servo = servos.get(json_item['wrist_rotate_label'])

        self.arm_list.append(Arm(json_item['label'], base_servo, shoulder_servo, elbow_servo,
                                 wrist_servo, wrist_rotate_servo))

    def get_includes(self):
        return "#include \"Arm.h\";"

    def get_constructor(self):
        rv = "Arm arms[{0:d}] = {{\n".format(len(self.arm_list))
        for arm in self.arm_list:
            rv += ("\tArm({0:s}_index, {1:s}_index, {2:s}_index, {3:s}_index, {4:s}_index, " +
                   "servo_pins, servos),\n").format(arm.base.label, arm.shoulder.label,
                                                    arm.elbow.label, arm.wrist.label,
                                                    arm.wrist_rotate.label)
        rv = rv[:-2] + "\n}};\n"
        return rv

    def get_response_block(self):
        return '''\t\telse if(args[0].equals(String("sa"))) {{ // set arm
        if(numArgs == 7) {{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}){{
                int posbase = args[2].toInt();
                int posshoulder = args[3].toInt();
                int poselbow = args[4].toInt();
                int poswrist = args[5].toInt();
                int poswristrotate = args[6].toInt();

                arms[indexNum].set(posbase, posshoulder, poselbow, poswrist, poswristrotate);
                Serial.println("ok");
            }} else {{
                Serial.println("error: usage - 'sa [id] [base] [shoulder] [elbow] [wrist] [wristrotate]'");
            }}
        }} else {{
            Serial.println("error: usage - 'sa [id] [base] [shoulder] [elbow] [wrist] [wristrotate]'");
        }}
    }}
    else if(args[0].equals(String("das"))) {{ // detach arm servos
        if(numArgs == 2) {{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}){{
                arms[indexNum].detach();
                Serial.println("ok");
            }} else {{
                Serial.println("error: usage - 'ds [id]'");
            }}
        }} else {{
            Serial.println("error: usage - 'ds [id]'");
        }}
    }}
'''.format(len(self.arm_list))

    def get_indices(self):
        for i, arm in enumerate(self.armList):
            yield i, arm
