class i2cencoder:
    def __init__(self, label, pinA, pinB, reverse, init_number):
        self.label = label
        self.pinA = pinA
        self.pinB = pinB
        self.reverse = reverse
        self.init_number = init_number


class i2cencoders:
    def __init__(self):
        self.sensor_list = []

    def add(self, json_item):
        self.sensor_list.append(i2cencoder(json_item['label'], json_item['pinA'], json_item['pinB'], json_item['reverse'], json_item['init_number']))
        self.sensor_list.sort(key=lambda x: x.init_number, reverse=False)


    def get_include(self):
        return "#include \"Wire.h\";\n#include \"I2CEncoder.h\";"

    def get_pins(self):
        rv = ""
        for sensor in self.sensor_list:
            rv = rv + "const char %s_pinA = %d;\n" % (sensor.label, sensor.pinA)
            rv = rv + "const char %s_pinB = %d;\n" % (sensor.label, sensor.pinB)
        return rv

    def get_constructor(self):
        rv = ""
        for i in range(len(self.sensor_list)):
            rv = rv + "const char %s_index = %d;\n" % (self.sensor_list[i].label, i)
        rv = rv + "I2CEncoder i2cencoders[%d];\n" % (len(self.sensor_list))
        return rv

    def get_setup(self):
        rv = "    Wire.begin();\n"
        for sensor in self.sensor_list:
            rv = rv + "    i2cencoders[%s_index].init(MOTOR_393_TORQUE_ROTATIONS, MOTOR_393_TIME_DELTA);\n" % sensor.label
        for sensor in self.sensor_list:
            if sensor.reverse:
                rv = rv + "    i2cencoders[%s_index].setReversed(true);\n" % sensor.label
        for sensor in self.sensor_list:
            rv = rv + "    i2cencoders[%s_index].zero();\n" % sensor.label
        rv = rv + "\n"
        return rv

    def get_response_block(self):
        return '''    else if(args[0].equals(String("ep"))){ // i2c encoder position (in rotations)
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                char dts[256];
                dtostrf(i2cencoders[indexNum].getPosition(), 0, 6, dts);
                Serial.println(dts);
            } else {
                Serial.println("Error: usage - ep [id]");
            }
        } else {
            Serial.println("Error: usage - ep [id]");
        }
    }
    else if(args[0].equals(String("erp"))){ // i2c encoder raw position (in ticks)
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                char dts[256];
                dtostrf(i2cencoders[indexNum].getRawPosition(), 0, 6, dts);
                Serial.println(dts);
            } else {
                Serial.println("Error: usage - erp [id]");
            }
        } else {
            Serial.println("Error: usage - erp [id]");
        }
    }
    else if(args[0].equals(String("es"))){ // i2c encoder speed (in revolutions per minute)
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                char dts[256];
                dtostrf(i2cencoders[indexNum].getSpeed(), 0, 6, dts);
                Serial.println(dts);
            } else {
                Serial.println("Error: usage - es [id]");
            }
        } else {
            Serial.println("Error: usage - es [id]");
        }
    }
    else if(args[0].equals(String("ez"))){ // i2c encoder zero
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                i2cencoders[indexNum].zero();
                Serial.println("ok");
            } else {
                Serial.println("Error: usage - ez [id]");
            }
        } else {
            Serial.println("Error: usage - ez [id]");
        }
    }
''' % (len(self.sensor_list), len(self.sensor_list), len(self.sensor_list), len(self.sensor_list))