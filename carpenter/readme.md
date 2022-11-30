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

mx = bp.stepper_motor(version="1234", zero=True, position_sensor=True)
mx.zero()  # use the limit switches to find zero
mx.cw(7)   # move clockwise 7 steps
mx.ccw(20rpm)

print(mx.position)  # show the current expected position of the motor in degrees and steps from zero
print(mx.sensed_position)  # show the current sensed position of the motor in degrees and steps from zero
print(mx.specs)   # show the values within which the motor can operate, including step resolution, max speed, microstepping options, etc.

ui = bp.server(wap=True, ssid="mydevice", password="password")
ui.write(mx.specs)

speed = ui.

forward = ui.btn("Forward", do=mx.cw())
reverse = ui.btn("Reverse", do=mx.ccw())


```
