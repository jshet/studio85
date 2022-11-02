# Carpenter is a framework for quickly assembling machines and their interfaces

The purpose of Carpenter is to add a layer of abstraction between hardware drivers and application logic.  
Decoupling specific drivers allows for longer term code stability. 
Instead of rewriting applications, only the Carpenter classes need modification. 

## Things Carpenter might handle

- sending commands to peripherals (displays, motors, switches, speakers, lights, etc.)
- receiving values from peripherals (buttons, switches, sensors, and other encoders)
- sending values to users (api, webhook, web interface, display, speaker)
- receiving commands from users

## Some examples

```
from Carpenter import blueprints as bp
from Carpenter import interfaces as ui

motor_x = bp.stepper_motor(version="1234", zero=True, position_sensor=True)
motor_x.zero()  # use the limit switches to find zero
motor_x.cw(7)   # move clockwise 7 steps
motor_x.ccw(20rpm)

print(motor_x.position)  # show the current expected position of the motor in degrees and steps from zero
print(motor_x.sensed_position)  # show the current sensed position of the motor in degrees and steps from zero
print(motor_x.specs)   # show the values within which the motor can operate, including step resolution, max speed, microstepping options, etc.

ui = bp.server(wap=True, ssid="mydevice", password="password")
ui.write(motor_x.specs)

speed = ui.

forward = ui.btn("Forward", do=motor_x.cw())
reverse = ui.btn("Reverse", do=motor_x.ccw())


```
