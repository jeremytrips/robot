
# Labibot

### context
School project in which an autonomous robot has to leave a maze by itself.
We had at our disposition:
* Arduino 
* Rasperry-pi
* US sensor
* IR sensor

We decided to use the pi as the Raspberry pi as the brain and an arduino to control robot dc motors. Moreover the pi would allow us to interface the state of the robot.
The basics idea was to use the left hand rule and follow a black line with the infra-red sensor and use the ulatra-sonic sensor to check wheter there was a wall in front of it. If there was a wall, which means that the robot reached a dead end, the robot has to make a turn around and then continue his way. 

Unfortunally, the project was unsuccessfull, after reevaluation some big mistake were pointed out:
* Infra-red sensor
The pi as only digital inputn, it would have be much easier to use the pinout of the arduino to read the analog value of the infrared sensor. By doing that we would have use another regulation system that a TOR. 
* The brain
The code used an event driven architecture. An event was fire each time the ir-sensor dropped. Each computation was done on the raspberry and the resulted move was then send to the arduino which, in some cases might work, but it was way to much complex for the project.
## Authors

* **Vincent Fischer** - https://github.com/Division01
* **Jeremy Trips**
