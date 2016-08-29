class fourwheeldrivebase:
    def __init__(self, label, useVelocityControl, lf_motor, rf_motor, lb_motor, rb_motor):
        self.lf_motor = lf_motor
        self.rf_motor = rf_motor
        self.lb_motor = lb_motor
        self.rb_motor = rb_motor
        self.useVelocityControl = useVelocityControl


class fourwheeldrivebaseList:
    def __init__(self):
        self.tier = 3
        self.drivebase_list = []

    def add(self, json_item, motors, velocitycontrolledmotors):
        useVelocityControl = json_item['useVelocityControl']

        if self.useVelocityControl:
            lf_motor = velocitycontrolledmotors.get[json_item['leftFrontDriveMotor']]
            rf_motor = velocitycontrolledmotors.get[json_item['rightFrontDriveMotor']]
            lb_motor = velocitycontrolledmotors.get[json_item['leftBackDriveMotor']]
            rb_motor = velocitycontrolledmotors.get[json_item['rightBackDriveMotor']]
        else:
            lf_motor = motors.get[json_item['leftFrontDriveMotor']]
            rf_motor = motors.get[json_item['rightFrontDriveMotor']]
            lb_motor = motors.get[json_item['leftBackDriveMotor']]
            rb_motor = motors.get[json_item['rightBackDriveMotor']]

        self.drivebase_list.append(fourwheeldrivebase(json_item['label'], useVelocityControl, lf_motor, rf_motor, lb_motor, rb_motor))

    def get_includes(self):
        return "#include \"FourWheelDrive.h\""

    def get_include_files(self):
        return ['FourWheelDrive.h', 'FourWheelDrive.cpp']

    def get_pins(self):
        return ""

    def get_constructor(self):
        rv = "FourWheelDrive fwds = {\n" % len(self.drivebase_list)
        for drivebase in self.drivebase_list:
            if drivebase.useVelocityControl:
                rv += "    FourWheelDrive(vcms[%s_index], vcms[%s_index], vcms[%s_index], vcms[%s_index]),\n" % (drivebase.lf_motor.label, drivebase.rf_motor.label, drivebase.lb_motor.label, drivebase.rb_motor.label)
            else:
                rv += "    FourWheelDrive(motors[%s_index], motors[%s_index], motors[%s_index], motors[%s_index]),\n" % (drivebase.lf_motor.label, drivebase.rf_motor.label, drivebase.lb_motor.label, drivebase.rb_motor.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        return ""

    def get_loop_functions(self):
        return ""

    def get_response_block(self):
        length = len(self.actuator_list)
        return '''    else if(args[0].equals(String("dfwd"))){ // drive four wheel drivebase
        if(numArgs == 6){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                int leftfront = args[2].toInt();
                int rightfront = args[3].toInt();
                int leftback = args[4].toInt();
                int rightback = args[5].toInt();

                if(leftfront > -1024 && leftfront < 1024 && rightfront > -1024 && rightfront < 1024 && leftback > -1024 && leftback < 1024 && rightback > -1024 && rightback < 1024) {
                    fwds[indexNum].drive(leftfront, rightfront, leftback, rightback)
                    Serial.println("ok");
                } else {
                    Serial.println("Error: usage - dfwd [id] [left front value] [right front value] [left back value] [right back value]");
                }
            } else {
                Serial.println("Error: usage - dfwd [id] [left front value] [right front value] [left back value] [right back value]");
            }
        } else {
            Serial.println("Error: usage - dfwd [id] [left front value] [right front value] [left back value] [right back value]");
        }
    }
    else if(args[0].equals(String("sfwd"))){ // stop four wheel drivebase
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                fwds[indexNum].stop()
                Serial.println("ok");
            } else {
                Serial.println("Error: usage - sfwd [id]");
            }
        } else {
            Serial.println("Error: usage - sfwd [id]");
        }
    }
    else if(args[0].equals(String("dfwdp"))){ // drive four wheel drivebase with pid
        if(numArgs == 6){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                double leftfront = toDouble(args[2]);
                double rightfront = toDouble(args[3]);
                double leftback = toDouble(args[4]);
                double rightback = toDouble(args[5]);

                fwds[indexNum].drivePID(leftfront, rightfront, leftback, rightback)
                Serial.println("ok");
            } else {
                Serial.println("Error: usage - dfwdp [id] [left front value] [right front value] [left back value] [right back value]");
            }
        } else {
            Serial.println("Error: usage - dfwdp [id] [left front value] [right front value] [left back value] [right back value]");
        }
    }
    else if(args[0].equals(String("fwdfl"))){ // get left side position
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                char dts[256];
                dtostrf(fwds[indexNum].getLeftPosition(), 0, 6, dts);
                Serial.println(dts);
            } else {
                Serial.println("Error: usage - dfwdp [id]");
            }
        } else {
            Serial.println("Error: usage - dfwdp [id]");
        }
    }
    else if(args[0].equals(String("fwdgr"))){ // get right side position
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                char dts[256];
                dtostrf(fwds[indexNum].getRightPosition(), 0, 6, dts);
                Serial.println(dts);
            } else {
                Serial.println("Error: usage - fwdgr [id]");
            }
        } else {
            Serial.println("Error: usage - fwdgr [id]");
        }
    }
''' % (length, length, length)

    def get_extra_functions(self):
        return ""
