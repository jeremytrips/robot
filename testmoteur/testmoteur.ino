#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

/*
 * This script was used to check wether dc motors where
 * working correctly.
 */

// Décommenter si inverser
//#define BACKWARD FORWARD
//#define FORWARD BACKWARD

#define DEFAULT_SPEED 100
#define SPEED_DELTA 30

void rotateRight();
void rotateLeft();

Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *MotorR = AFMS.getMotor(4);
Adafruit_DCMotor *MotorL = AFMS.getMotor(1);

int rotateTimeToWait = 100;
int redirectTimeToWait = 100;

void setup() {
  Serial.begin(9600);           
  AFMS.begin();
  MotorR->setSpeed(DEFAULT_SPEED);
  MotorL->setSpeed(DEFAULT_SPEED);

  MotorR->run(RELEASE);
  
  MotorL->run(FORWARD);
  Serial.readStringUntil('%');
  MotorL->run(BACKWARD);
  Serial.readStringUntil('%');

  MotorL->run(RELEASE);

  MotorR->run(FORWARD);
  Serial.readStringUntil('%');
  MotorR->run(BACKWARD);
  Serial.readStringUntil('%');  

  Serial.println("Enter a command>");
}

void loop(){
  if (Serial.available()){
    int a = Serial.readStringUntil('%').toInt();
    switch (a)  
    {
    case 0:
      rotateLeft();
      break;
    case 1:
      rotateRight();
      break;
    case 2:
      while(!Serial.available());
      delay(50);
      rotateTimeToWait = Serial.readStringUntil('%').toInt();
      break;
    case 3:
      while(!Serial.available());
      delay(50);
      redirectTimeToWait = Serial.readStringUntil('%').toInt();
      break;
    default:
      break;
    }
  }
}

void forward(){
  MotorR->run(FORWARD);
  MotorL->run(FORWARD);
}


void redirectRight(){
  MotorR->setSpeed(DEFAULT_SPEED);
  MotorL->setSpeed(DEFAULT_SPEED-SPEED_DELTA);
  delay(redirectTimeToWait);
  MotorR->setSpeed(DEFAULT_SPEED);
  MotorL->setSpeed(DEFAULT_SPEED);
}


void redirectLeft(){
  MotorR->setSpeed(DEFAULT_SPEED-SPEED_DELTA);
  MotorL->setSpeed(DEFAULT_SPEED);
  delay(redirectTimeToWait);
  MotorR->setSpeed(DEFAULT_SPEED);
  MotorL->setSpeed(DEFAULT_SPEED);
}

void rotateRight(){
  MotorR->run(BACKWARD);
  MotorL->run(FORWARD);
  delay(rotateTimeToWait);
  forward();
}

void rotateLeft(){
  MotorR->run(FORWARD);
  MotorL->run(BACKWARD);
  delay(rotateTimeToWait);
  forward();
}