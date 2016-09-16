from appendages.i2c_encoder_list import I2CEncoder
from appendages.component_list import ComponentList


class VelocityControlledMotor:
    def __init__(self, label, motor, encoder, vpid):
        self.label = label
        self.motor = motor
        self.encoder = encoder
        self.vpid = vpid


class VelocityControlledMotorList(ComponentList):
    TIER = 2

    def __init__(self):
        self.vcmDict = {}
        self.vcmList = []

    def add(self, json_item, motors, i2cencoders, encoders, vpids):
        motor = motors.get(json_item['motor_label'])
        encoder = None
        if i2cencoders is not None:
            encoder = i2cencoders.get(json_item['encoder_label'])
        if encoder is None:
            encoder = encoders.get(json_item['encoder_label'])
        vpid = vpids.get(json_item['vpid_label'])
        vcm = VelocityControlledMotor(json_item['label'], motor, encoder, vpid)
        self.vcmDict[json_item['label']] = vcm
        self.vcmList.append(vcm)
        self.vcmList.sort(key=lambda x: x.label, reverse=False)

    def get(self, label):
        if label in self.vcmDict:
            return self.vcmDict[label]
        else:
            return None

    def get_includes(self):
        return "#include \"VelocityControlledMotor.h\";"

    def get_constructor(self):
        rv = ""
        for i, vcm in enumerate(self.vcmList):
            rv += "const char {0:s}_index = {1:d};\n".format(vcm.label, i)
        rv += "VelocityControlledMotor vcms[{0:d}] = {{\n".format(len(self.vcmList))
        for vcm in self.vcmList:
            if isinstance(vcm.encoder, I2CEncoder):
                rv += ("\tVelocityControlledMotor(motors[{0:s}_index], i2cencoders[{1:s}_index], " +
                       "vpids[{2:s}_index], &Inputs_vpid[{2:s}_index], " +
                       "&Setpoints_vpid[{2:s}_index], &Outputs_vpid[{2:s}_index]),\n")\
                        .format(vcm.motor.label, vcm.encoder.label, vcm.vpid.label)
            else:
                rv += ("\tVelocityControlledMotor(motors[{0:s}_index], encoders[{1:s}_index], " +
                       "vpids[{2:s}_index], &Inputs_vpid[{2:s}_index], " +
                       "&Setpoints_vpid[{2:s}_index], &Outputs_vpid[{2:s}_index]),\n")\
                        .format(vcm.motor.label, vcm.encoder.label, vcm.vpid.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_loop_functions(self):
        return "for(int i = 0; i < {0:d}; i++) {{\n\t\t\tvcms[i].runVPID();\n\t\t}}\n".format(
            len(self.vcmList))

    def get_response_block(self):
        length = len(self.vcmList)
        return '''\t\telse if(args[0].equals(String("vcmd"))) {{ // set velocity controlled motor voltage (no pid)
        if(numArgs == 7) {{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}){{
                int value = args[2].toInt();
                if( value < -1023 || value > 1023) {{
                    Serial.println("Error: usage - vcmd [id] [value]");
                }} else {{
                    vcms[indexNum].setValue(value);
                    Serial.println("ok");
                }}
            }} else {{
                Serial.println("error: usage - 'vcmd [id] [value]'");
            }}
        }} else {{
            Serial.println("error: usage - 'vcmd [id] [value]'");
        }}
    }}
    else if(args[0].equals(String("vcms"))){{ // set velocity controlled motor to stop
        if(numArgs == 2) {{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}) {{
                vcms[indexNum].stop();
                Serial.println("ok");
            }} else {{
                Serial.println("Error: usage - vcms [id]");
            }}
        }} else {{
            Serial.println("Error: usage - vcms [id]");
        }}
    }}
    else if(args[0].equals(String("vcmsv"))){{ // set velocity controlled motor's velocity
        if(numArgs == 3) {{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}) {{
                vcms[indexNum].setVelocity(toDouble(args[2]));
                Serial.println("ok");
            }} else {{
                Serial.println("Error: usage - vcmsv [id] [vel]");
            }}
        }} else {{
            Serial.println("Error: usage - vcmsv [id] [vel]");
        }}
    }}
    else if(args[0].equals(String("vcmgv"))){{ // get velocity controlled motor's velocity
        if(numArgs == 2) {{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}) {{
                char dts[256];
                dtostrf(vcms[indexNum].getVelocity(), 0, 6, dts);
                Serial.println(dts);
            }} else {{
                Serial.println("Error: usage - vcmgv [id]");
            }}
        }} else {{
            Serial.println("Error: usage - vcmgv [id]");
        }}
    }}
    else if(args[0].equals(String("vcmgp"))){{ // get velocity controlled motor's position
        if(numArgs == 2) {{
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < {0:d}) {{
                char dts[256];
                dtostrf(vcms[indexNum].getPosition(), 0, 6, dts);
                Serial.println(dts);
            }} else {{
                Serial.println("Error: usage - vcmgp [id]");
            }}
        }} else {{
            Serial.println("Error: usage - vcmgp [id]");
        }}
    }}
'''.format(length)

    def get_indices(self):
        for i, vcm in enumerate(self.vcmList):
            yield i, vcm