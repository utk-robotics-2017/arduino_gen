#ifndef MOTOR_h
#define MOTOR_h

enum MotorControllerType {
	MonsterMoto,
	RoverFive
};

class Motor
{
public:
	Motor(char, char, char, char, MotorControllerType);
	void drive(int);
	void stop();

private:
	char inA, inB, pwm, reverse;
	MotorControllerType type;
};


#endif
