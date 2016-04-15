# ArduinoGen
Arduino Code Generator for the UTK IEEE General Robot Platform


## Sensors

#### Linesensor
	label - name associated with the sensor
	pin - signal pin connected to the sensor

#### Linesensor Arrays
	*** Work in progress ***

#### Ultrasonics
	label - name associated with the sensor
	pin - signal pin connected to the sensor

#### Switches (Any kind of switch or button)
	label - name associated with the sensor
	pin - signal pin connected to the sensor

#### I2C Encoders
	label - name associated with the sensor
	pinA - signal A pin connected to the sensor
	pinB - signal B pin connected to the sensor
	reverse - whether the direction of the encoder needs to be reversed
	init_number - the number of the I2C encoder in the chain

#### Encoders
	label - name associated with the sensor
	pinA - signal A pin connected to the sensor
	pinB - signal B pin connected to the sensor


## Actuators

#### Servo
	label - name associated with servo
	pin - signal pin connected to the servo

#### Monster Moto Motor
	label - name associated with the motor
	inA_pin - one of the signal pins used for direction
	inB_pin - other signal pin used for direction
	pwm_pin - signal pin for speed
	reverse - whether the direction of the motor needs to be reversed


## Special

#### Lynxmotion Arm
	label - name associated with the arm
	base_pin - signal pin for controling the servo in the base
	shoulder_pin - signal pin for controling the servo in the shoulder
	elbow_pin - signal pin for controling the servo in the elbow
	wrist_pin - signal pin for controling the servo in the write
	wrist_rotate_pin - signal pin for controling the servo in the write that handles rotating the wrist
