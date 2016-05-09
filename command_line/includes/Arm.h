#ifndef ARM_h
#define ARM_h

#include "Servo.h"

class Arm
{
public:
	Arm(char, char, char, char, char, char*, Servo*);
	void set(int, int, int, int, int);
	void detach();

private:
	char base_index, shoulder_index, elbow_index, wrist_index, wrist_rot_index;
	char* pins;
	Servo* servos;
};

#endif