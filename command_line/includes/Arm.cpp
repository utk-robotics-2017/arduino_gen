#include "Arm.h"

Arm::Arm(char base_index, char shoulder_index, char elbow_index, char wrist_index, char wrist_rot_index, char* pins, Servo* servos)
{
	this->base_index = base_index;
	this->shoulder_index = shoulder_index;
	this->elbow_index = elbow_index;
	this->wrist_index = wrist_index;
	this->wrist_rot_index = wrist_rot_index;
	this->pins = pins;
	this->servos = servos;
}

void Arm::set(int base, int shoulder, int elbow, int wrist, int wrist_rot)
{
	if(!servos[base_index].attached())
	{
		servos[base_index].attach(pins[base_index]);
		servos[shoulder_index].attach(pins[shoulder_index]);
		servos[elbow_index].attach(pins[elbow_index]);
		servos[wrist_index].attach(pins[wrist_index]);
		servos[wrist_rot_index].attach(pins[wrist_rot_index]);
	}

	servos[base_index].write(base);
	servos[shoulder_index].write(shoulder);
	servos[elbow_index].write(elbow);
	servos[wrist_index].write(wrist);
	servos[wrist_rot_index].write(wrist_rot);
}

void Arm::detach()
{
	servos[base_index].detach();
	servos[shoulder_index].detach();
	servos[elbow_index].detach();
	servos[wrist_index].detach();
	servos[wrist_rot_index].detach();
}