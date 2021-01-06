#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

#define BACKWARD 1
#define FORWARD 2


Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *MotorR = AFMS.getMotor(4);
Adafruit_DCMotor *MotorL = AFMS.getMotor(1);

int msg;


void setup() {
  Serial.begin(9600);           
  AFMS.begin();
}

void loop() {
  msg = readSerialPort();
  switch (msg) {
    case 0:
      Stop();
      break;
    case 1:
      MoveForward();
      break;
    case 2:
      rotateLeft();
      break;  
    case 3:
      rotateRight();
      break;
     case 4:
      Back();
      break;
  }
}

void rotateRight(){
  MotorR->setSpeed(50);
  MotorL->setSpeed(50);
  MotorR->run(BACKWARD);
  MotorL->run(FORWARD);
}

void rotateLeft(){
  MotorR->setSpeed(50);
  MotorL->setSpeed(50);
  MotorR->run(FORWARD);
  MotorL->run(BACKWARD);
}


void MoveForward(){
  MotorR->setSpeed(125);
  MotorL->setSpeed(125);
  MotorR->run(FORWARD);
  MotorL->run(FORWARD);
}

void Back(){
  MotorR->setSpeed(125);
  MotorL->setSpeed(125);
  MotorR->run(BACKWARD);
  MotorL->run(BACKWARD);
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
