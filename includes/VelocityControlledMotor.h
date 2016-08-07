#ifndef VELOCITYCONTROLLEDMOTOR_h
#define VELOCITYCONTROLLEDMOTOR_h

#include "Motor.h"
#include "I2CEncoder.h"
#include "Encoder.h"
#include "VPID.h"

class VelocityControlledMotor
{
public:
	VelocityControlledMotor(Motor, I2CEncoder, VPID);

	void setValue(int);
	void setVelocity(double);
	void stop();

	double getVelocity();
	double getPosition();
private:
	Motor motor;
	Encoder encoder;
	I2CEncoder i2cEncoder;
	VPID vpid;
};

#endif