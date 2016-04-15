class encoder:
    def __init__(self, label, pinA, pinB):
        self.label = label
        self.pinA = pinA
        self.pinB = pinB


class encoders:
    def __init__(self):
        self.sensor_list = []

    def add(self, json_item):
        self.sensor_list.append(encoder(json_item['label'], json_item['pinA'], json_item['pinB']))

    def get_include(self):
        return "#include \"Encoder.h\";"

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
        rv = rv + "Encoder encoders[%d] = {\n" % len(self.sensor_list)

        for sensor in self.sensor_list:
            rv = rv + "    Encoder(%s_pinA, %s_pinB),\n" % (sensor.label, sensor.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_setup(self):
        return ""

    def get_response_block(self):
        return '''    else if(args[0].equals(String("re"))){ // read encoders
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                Serial.println(encoders[indexNum].read());
            } else {
                Serial.println("Error: usage - re [id]");
            }
        } else {
            Serial.println("Error: usage - re [id]");
        }
    }
    else if(args[0].equals(String("ze"))){ // zero encoders
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < %d){
                encoders[indexNum].write(0);
                Serial.println("ok");
            } else {
                Serial.println("Error: usage - ze [id]");
            }
        } else {
            Serial.println("Error: usage - ze [id]");
        }
    }
''' % (len(self.sensor_list), len(self.sensor_list))
