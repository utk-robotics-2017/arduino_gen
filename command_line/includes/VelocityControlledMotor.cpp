#include "MotorEncoderPID.h"

VelocityControlledMotor::VelocityControlledMotor(Motor motor, I2CEncoder encoder, VPID vpid, double* input, double* setpoint, double* output)
{
	this->i2c = 1;
	this->motor = motor;
	this->i2cEncoder = encoder;
	this->vpid = vpid;

	this->input = input;
	this->setpoint = setpoint;
	this->output = output;
}

void VelocityControlledMotor::setValue(int value)
{
	vpid.setMode(MANUAL);
	motor.drive(value);
}
	
void VelocityControlledMotor::setVelocity(double velocity);
{
	setpoint = velocity;
	vpid.setMode(AUTO);
}

void VelocityControlledMotor::stop()
{
	vpid.setMode(MANUAL);
	setValue(0);
}

void VelocityControlledMotor::runVPID()
{
	input = getVelocity();
	char updated = vpid.calculate();
	if(updated) {
		motor.drive(output);
	}
}

double VelocityControlledMotor::getVelocity()
{
	return i2cencoder.getVelocity();
}

double VelocityControlledMotor::getPosition()
{
	return i2cencoder.getPosition();
}