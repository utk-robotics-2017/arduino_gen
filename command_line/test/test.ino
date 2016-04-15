// Auto-generated by ArduinoGen

// Includes
#include "Encoder.h";
#include "Servo.h";
#include "NewPing.h";
#include "Wire.h";
#include "I2CEncoder.h";

#define STR1(x)  #x
#define STR(x)  STR1(x)

// Globals
int ledState = HIGH;
// Command parsing
const int MAX_ARGS = 6;
String args[MAX_ARGS];
int numArgs = 0;

// Pin definitions
const char LED = 13;
const char right_front_wheel_encoder_pinA = 35;
const char right_front_wheel_encoder_pinB = 36;

const char test_servo_pin = 4;

const char course_switch_pin = 35;
const char lift_switch_pin = 35;
const char a_button_pin = 35;

const char front_ultrasonic_pin = 22;
const char left_ultrasonic_pin = 23;

const char left_front_wheel_encoder_pinA = 33;
const char left_front_wheel_encoder_pinB = 34;

const char left_linesensor_pin = 2;


// Constructors
Encoder encoders[1] = {
    Encoder(right_front_wheel_encoder_pinA, right_front_wheel_encoder_pinB)
};

const char test_servo_index = 0;
Servo servos[1];

const char course_switch_index = 0;
const char lift_switch_index = 1;
const char a_button_index = 2;
char switches[3] = {
    course_switch_pin,
    lift_switch_pin,
    a_button_pin
};

NewPing ultrasonics[2] = {
    NewPing(front_ultrasonic_pin, front_ultrasonic_pin),
    NewPing(left_ultrasonic_pin, left_ultrasonic_pin)
};

const char left_front_wheel_encoder_index = 0;
I2CEncoder i2cencoders[1];

char linesensors[1] = {
    left_linesensor_pin
};


void setup() {
    // Init LED pin
    pinMode(LED, OUTPUT);

    servos[test_servo_index].attach(test_servo_pin);

    pinMode(course_switch_pin, INPUT_PULLUP);
    pinMode(lift_switch_pin, INPUT);
    pinMode(a_button_pin, INPUT_PULLUP);

    Wire.begin();
    i2cencoders[left_front_wheel_encoder_index].init(MOTOR_393_TORQUE_ROTATIONS, MOTOR_393_TIME_DELTA);
    i2cencoders[left_front_wheel_encoder_index].zero();

    //Init Serial
    Serial.begin(115200);
}

/* The loop is set up in two parts. First the Arduino does the work it needs to
 * do for every loop, next is runs the checkInput() routine to check and act on
 * any input from the serial connection.
 */
void loop() {
    int inbyte;

    // Accept and parse serial input
    checkInput();
}

void parse_args(String command) {
    numArgs = 0;
    int beginIdx = 0;
    int idx = command.indexOf(" ");

    String arg;
    char charBuffer[16];

    while (idx != -1)
    {
        arg = command.substring(beginIdx, idx);

        // add error handling for atoi:
        args[numArgs++] = arg;
        beginIdx = idx + 1;
        idx = command.indexOf(" ", beginIdx);
    }

    arg = command.substring(beginIdx);
    args[numArgs++] = arg;
}

/* This routine checks for any input waiting on the serial line. If any is
 * available it is read in and added to a 128 character buffer. It sends back
 * an error should the buffer overflow, and starts overwriting the buffer
 * at that point. It only reads one character per call. If it receives a
 * newline character is then runs the parseAndExecuteCommand() routine.
 */
void checkInput() {
    int inbyte;
    static char incomingBuffer[128];
    static char bufPosition=0;

    if(Serial.available()>0) {
        // Read only one character per call
        inbyte = Serial.read();
        if(inbyte==10||inbyte==13) {
            // Newline detected
            incomingBuffer[bufPosition]='\0'; // NULL terminate the string
            bufPosition=0; // Prepare for next command

            // Supply a separate routine for parsing the command. This will
            // vary depending on the task.
            parseAndExecuteCommand(String(incomingBuffer));
        }
        else {
            incomingBuffer[bufPosition]=(char)inbyte;
            bufPosition++;
            if(bufPosition==128) {
                Serial.println("error: command overflow");
                bufPosition=0;
            }
        }
    }
}

/* This routine parses and executes any command received. It will have to be
 * rewritten for any sketch to use the appropriate commands and arguments for
 * the program you design. I find it easier to separate the input assembly
 * from parsing so that I only have to modify this function and can keep the
 * checkInput() function the same in each sketch.
 */
void parseAndExecuteCommand(String command) {
    Serial.println("> " + command);
    parse_args(command);
    if(args[0].equals(String("ping"))) {
        if(numArgs == 1) {
            Serial.println("ok");
        } else {
            Serial.println("error: usage - 'ping'");
        }
    }
    else if(args[0].equals(String("le"))) { // led set
        if(numArgs == 2) {
            if(args[1].equals(String("on"))) {
                ledState = HIGH;
                digitalWrite(LED,HIGH);
                Serial.println("ok");
            } else if(args[1].equals(String("off"))) {
                ledState = LOW;
                digitalWrite(LED,LOW);
                Serial.println("ok");
            } else {
                Serial.println("error: usage - 'le [on/off]'");
            }
        } else {
            Serial.println("error: usage - 'le [on/off]'");
        }
    }
    else if(args[0].equals(String("rl"))) { // read led
        if(numArgs == 1) {
            Serial.println(ledState);
        } else {
            Serial.println("error: usage - 'rl'");
        }
    }
    else if(args[0].equals(String("re"))){ // read encoders
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < 1){
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
            if(indexNum > -1 && indexNum < 1){
                encoders[indexNum].write(0);
                Serial.println("ok");
            } else {
                Serial.println("Error: usage - ze [id]");
            }
        } else {
            Serial.println("Error: usage - ze [id]");
        }
    }
    else if(args[0].equals(String("ss"))){ // set servo
        if(numArgs == 3){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < 1){
                int value = args[2].toInt();
                servos[indexNum].write(value);
                Serial.println("ok");
            } else {
                Serial.println("Error: usage - ss [id] [value]");
            }
        } else {
            Serial.println("Error: usage - ss [id] [value]");
        }
    }
    else if(args[0].equals(String("rs"))){ // read switches
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < 3){
                Serial.println(digitalRead(switches[indexNum]));
            } else {
                Serial.println("Error: usage - rs [id]");
            }
        } else {
            Serial.println("Error: usage - rs [id]");
        }
    }
    else if(args[0].equals(String("rus"))){ // read ultrasonics
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < 2){
                unsigned int response = ultrasonics[indexNum].ping();
                Serial.println(response);
            } else {
                Serial.println("Error: usage - rus [id]");
            }
        } else {
            Serial.println("Error: usage - rus [id]");
        }
    }
    else if(args[0].equals(String("ep"))){ // encoder position (in rotations)
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < 1){
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
            if(indexNum > -1 && indexNum < 1){
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
            if(indexNum > -1 && indexNum < 1){
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
            if(indexNum > -1 && indexNum < 1){
                i2cencoders[indexNum].zero();
                Serial.println("ok");
            } else {
                Serial.println("Error: usage - es [id]");
            }
        } else {
            Serial.println("Error: usage - es [id]");
        }
    }
    else if(args[0].equals(String("rls"))){ // read linesensors
        if(numArgs == 2){
            int indexNum = args[1].toInt();
            if(indexNum > -1 && indexNum < 1){
                Serial.println(analogRead(linesensors[indexNum]));
            } else {
                Serial.println("Error: usage - rls [id]");
            }
        } else {
            Serial.println("Error: usage - rls [id]");
        }
    }
    else if(args[0].equals(String("ver"))) { // version information
        if(numArgs == 1) {
            String out = "Source last modified: ";
            out += __TIMESTAMP__;
            out += "\r\nPreprocessor timestamp: " __DATE__ " " __TIME__;
            out += "\r\nSource code line number: ";
            out += __LINE__;
            out += "\r\nUsername: " STR(__USER__);
            out += "\r\nDirectory: " STR(__DIR__);
            out += "\r\nGit hash: " STR(__GIT_HASH__);
            Serial.println(out);
        } else {
            Serial.println("error: usage - 'ver'");
        }
    }
    else {
        // Unrecognized command
        Serial.println("error: unrecognized command");
    }
}
