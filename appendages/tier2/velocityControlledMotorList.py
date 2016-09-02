from ..i2cencoderList import i2cencoder

class velocitycontrolledmotor:
    def __init__(self, label, motor, encoder, vpid):
        self.label = label
        self.motor = motor
        self.encoder = encoder
        self.vpid = vpid


class velocityControlledMotorList:
    def __init__(self):
        self.tier = 2
        self.vcmDict = {}
        self.vcmList = []

    def add(self, json_item, motors, i2cencoders, encoders, vpids):
        motor = motors.get(json_item['motor_label'])
        encoder = None
        if not i2cencoders is None:
            encoder = i2cencoders.get(json_item['encoder_label'])
        if encoder is None:
            encoder = encoders.get(json_item['encoder_label'])
        vpid = vpids.get(json_item['vpid_label'])
        vcm = velocitycontrolledmotor(json_item['label'], motor, encoder, vpid)
        self.vcmDict[json_item['label']] = vcm
        self.vcmList.append(vcm)
        self.vcmList.sort(key=lambda x:x.label, reverse=False)

    def get_include(self):
        return "#include \"VelocityControlledMotor.h\";"

    def get_pins(self):
        return ""

    def get_constructor(self):
        rv = "VelocityControlledMotor vcms[%d] = {\n" % len(self.vcmList)
        for vcm in self.vcmList:
            if isinstance(vcm.encoder, i2cencoder):
                rv += "    VelocityControlledMotor(motors[%s_index], i2cencoders[%s_index], vpids[%s_index], &Inputs_vpid[%s_index], &Setpoints_vpid[%s_index], &Outputs_vpid[%s_index]),\n" % (vcm.motor.label, vcm.encoder.label, vcm.vpid.label, vcm.vpid.label, vcm.vpid.label, vcm.vpid.label)
            else:
                rv += "    VelocityControlledMotor(motors[%s_index], encoders[%s_index], vpids[%s_index], &Inputs_vpid[%s_index], &Setpoints_vpid[%s_index], &Outputs_vpid[%s_index]),\n" % (vcm.motor.label, vcm.encoder.label, vcm.vpid.label, vcm.vpid.label, vcm.vpid.label, vcm.vpid.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        return ""

    def get_loop_functions(self):
        return "for(int i = 0; i < %d; i++) {\n        vcms[i].runVPID();\n    }\n" % len(self.vcmList)

    def get_response_block(self):
        length = len(self.vcmList)
        return '''    else if(args[0].equals(String("vcmd"))) { // set velocity controlled motor voltage (no pid)
        if(numArgs == 7) {
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                int value = args[2].toInt();
                if( value < -1023 || value > 1023) {
                    Serial.println("Error: usage - vcmd [id] [value]");
                } else {
                    vcms[indexNum].setValue(value);
                    Serial.println("ok");
                }
            } else {
                Serial.println("error: usage - 'vcmd [id] [value]'");
            }
        } else {
            Serial.println("error: usage - 'vcmd [id] [value]'");
        }
    }
    else if(args[0].equals(String("vcms"))){ // set velocity controlled motor to stop
        if(numArgs == 2) {
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d) {
                vcms[indexNum].stop();
                Serial.println("ok");
            } else {
                Serial.println("Error: usage - vcms [id]");
            }
        } else {
            Serial.println("Error: usage - vcms [id]");
        }
    }
    else if(args[0].equals(String("vcmsv"))){ // set velocity controlled motor's velocity
        if(numArgs == 2) {
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d) {
                vcms[indexNum].setVelocity(toDouble(args[2]));
                Serial.println("ok");
            } else {
                Serial.println("Error: usage - vcms [id]");
            }
        } else {
            Serial.println("Error: usage - vcms [id]");
        }
    }
    else if(args[0].equals(String("vcmgv"))){ // get velocity controlled motor's velocity
        if(numArgs == 2) {
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d) {
                char dts[256];
                dtostrf(vcms[indexNum].getVelocity(), 0, 6, dts);
                Serial.println(dts);
            } else {
                Serial.println("Error: usage - vcmgv [id]");
            }
        } else {
            Serial.println("Error: usage - vcmgv [id]");
        }
    }
    else if(args[0].equals(String("vcmgp"))){ // get velocity controlled motor's position
        if(numArgs == 2) {
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d) {
                char dts[256];
                dtostrf(vcms[indexNum].getPosition(), 0, 6, dts);
                Serial.println(dts);
            } else {
                Serial.println("Error: usage - vcmgp [id]");
            }
        } else {
            Serial.println("Error: usage - vcmgp [id]");
        }
    }
''' % (length, length, length, length, length)

    def get_extra_functions(self):
        return ""

    def get_indices(self):
        for i, vcm in enumerate(self.vcmList):
            yield i, vcm
