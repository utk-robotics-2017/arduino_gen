class i2cencoder:
    def __init__(self, label, reverse, init_number):
        self.label = label
        self.reverse = reverse
        self.init_number = init_number


class i2cencoderList:
    def __init__(self):
        self.sensors = dict()
        self.sorted_sensors = []

    def add(self, json_item):
        sensor = i2cencoder(json_item['label'], json_item['reverse'], json_item['init_number'])
        self.sensors[json_item['label']] = sensor
        self.sorted_sensors.append(sensor)
        self.sorted_sensors.sort(key=lambda x: x.init_number, reverse=False)

    def get(self, label):
        return self.sensors[label]

    def get_include(self):
        return "#include <Wire.h>\n#include \"I2CEncoder.h\""

    def get_include_files(self):
        return ['I2CEncoder.h', 'I2CEncoder.cpp']

    def get_pins(self):
        return ""

    def get_constructor(self):
        rv = ""
        for i in range(len(self.sorted_sensors)):
            rv = rv + "const char %s_index = %d;\n" % (self.sorted_sensors[i].label, i)
        rv = rv + "I2CEncoder i2cencoders[%d];\n" % (len(self.sorted_sensors))
        return rv

    def get_setup(self):
        rv = "    Wire.begin();\n"
        for sensor in self.sorted_sensors:
            rv = rv + "    i2cencoders[%s_index].init(MOTOR_393_TORQUE_ROTATIONS, MOTOR_393_TIME_DELTA);\n" % sensor.label
        for sensor in self.sorted_sensors:
            if sensor.reverse:
                rv = rv + "    i2cencoders[%s_index].setReversed(true);\n" % sensor.label
        for sensor in self.sorted_sensors:
            rv = rv + "    i2cencoders[%s_index].zero();\n" % sensor.label
        rv = rv + "\n"
        return rv

    def get_loop_functions(self):
        return ""

    def get_response_block(self):

        numSensors = len(self.sorted_sensors)

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
    else if(args[0].equals(String("ev"))){ // i2c encoder velocity (in revolutions per minute)
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                char dts[256];
                dtostrf(i2cencoders[indexNum].getVelocity(), 0, 6, dts);
                Serial.println(dts);
            } else {
                Serial.println("Error: usage - ev [id]");
            }
        } else {
            Serial.println("Error: usage - ev [id]");
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
''' % (numSensors, numSensors, numSensors, numSensors, numSensors)

    def get_extra_functions(self):
        return ""
