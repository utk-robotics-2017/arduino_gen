class velocitycontrolledmotor:
    def __init__(self, label, motor, encoder, vpid):
        self.label = label
        self.motor = motor
        self.encoder = encoder
        self.vpid = vpid


class velocitycontrolledmotorList:
    def __init__(self):
        self.vcms = dict()

    def add(self, json_item, motors, encoders, vpids):
        motor = motors.get(json_item['motor_label'])
        encoder = encoders.get(json_item['encoder_label'])
        vpid = vpids.get(json_item['vpid_label'])
        self.vcms[json_item['label']] = velocitycontrolledmotor(json_item['label'], motor, encoder, vpid)

    def get_include(self):
        return "#include \"VelocityControlledMotor.h\";"

    def get_include_files(self):
        return ['VelocityControlledMotor.h', 'VelocityControlledMotor.cpp']

    def get_pins(self):
        return ""

    def get_constructor(self):
        rv = "VelocityControlledMotor vcms[%d] = {\n" % len(self.vcms)
        for vcm in self.vcms:
            rv += "    VelocityControlledMotor(motors[%_index], i2cencoders[%s_index], vpids[%s_index]),\n" % (vcm.motor.label, vcm.encoder.label, vcm.vpid.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        return ""

    def get_response_block(self):
        length = len(self.vcms)
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
                vcms[indexNum].setValue(toDouble(velcity));
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
