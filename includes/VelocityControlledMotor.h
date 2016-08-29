#ifndef VELOCITYCONTROLLEDMOTOR_h
#define VELOCITYCONTROLLEDMOTOR_h

#include "Motor.h"
#include "I2CEncoder.h"
#include "Encoder.h"
#include "VPID.h"

class VelocityControlledMotor
{
public:
	VelocityControlledMotor(Motor, I2CEncoder, VPID, double* input, double* setpoint, double* output);
    VelocityControlledMotor(Motor, Encoder, VPID, double* input, double* setpoint, double* output);

	void setValue(int);
	void setVelocity(double);
	void stop();

    void runVPID();

	double getVelocity();
	double getPosition();
private:
    bool i2c;

	Motor motor;
	Encoder encoder;
	I2CEncoder i2cEncoder;
	Encoder encoder;
    
    VPID vpid;
    double* input;
    double* setpoint;
    double* output;
};

#endif
