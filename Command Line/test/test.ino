#include "NewPing.h";

char ultrasonic1_pin = 22
char ultrasonic2_pin = 23

NewPing ultrasonic1 = new NewPing(ultrasonic1_pin, ultrasonic1_pin);
NewPing ultrasonic2 = new NewPing(ultrasonic2_pin, ultrasonic2_pin);
