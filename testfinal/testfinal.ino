#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

//#define BACKWARD FORWARD
//#define FORWARD BACKWARD

#define DEFAULT_SPEED 150
#define SPEED_DELTA 30
#define REDIRECT_TIME 150
#define ROTATE_TIME 150

Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *MotorR = AFMS.getMotor(4);
Adafruit_DCMotor *MotorL = AFMS.getMotor(1);

int msg;


void setup() {
  Serial.begin(9600);           
  AFMS.begin();
  MotorR->setSpeed(50);
  MotorL->setSpeed(50);
}

void loop() {
  msg = readSerialPort();
  switch (msg) {
    case 0:
      MoveForward();
      break;
    case 4:
      rotateRight();
      break;
    case 5:
      rotateLeft();
      break;  
    case 6:
      Stop();
      break;
    case 7:
      redirectRight();
      break;
    case 8:
      redirectLeft();
      break;
  }
}

void rotateRight(){
  MotorR->run(BACKWARD);
  MotorL->run(FORWARD);
}

void rotateLeft(){
  MotorR->run(FORWARD);
  MotorL->run(BACKWARD);
}

void redirectRight(){
  MotorR->setSpeed(DEFAULT_SPEED);
  MotorL->setSpeed(DEFAULT_SPEED-SPEED_DELTA);
  delay(REDIRECT_TIME);
  MoveForward();
}


void redirectLeft(){
  MotorR->setSpeed(DEFAULT_SPEED-SPEED_DELTA);
  MotorL->setSpeed(DEFAULT_SPEED);
  delay(REDIRECT_TIME);
  MoveForward();
}


void MoveForward(){
  MotorR->setSpeed(DEFAULT_SPEED);
  MotorL->setSpeed(DEFAULT_SPEED);
  MotorR->run(FORWARD);
  MotorL->run(FORWARD);
}

void Stop(){
  MotorR->run(RELEASE);
  MotorL->run(RELEASE);
}

int readSerialPort() {
  if (Serial.available()) {
    delay(10);
      return Serial.readStringUntil('%').toInt();
  } 
  else {
    return 10;
  }
}
