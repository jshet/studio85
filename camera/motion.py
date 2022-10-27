from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
from time import sleep

motors = MotorKit()

min_position = 0
max_position = 1200
backlash_comp = 10

def forward(steps, step_delay=0.01):
    for i in range(steps):
        motors.stepper1.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
        print(f"+{i}")
        sleep(step_delay)
    motors.stepper1.release()

def backward(steps, step_delay=0.01):
    for i in range(steps):
        motors.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
        print(f"-{i}")
        sleep(step_delay)
    motors.stepper1.release()

def compensate_backlash(last_moved="forward"):
    print("Compensating for backlash...")
    backward(backlash_comp) if last_moved == "forward" else forward(backlash_comp)

def move(steps, start_position):
    if steps + start_position in range(min_position, max_position):
        forward(steps) if 0 < steps else backward((0 - steps))
        end_position = start_position + steps
        print(f"Moved {steps} steps from {start_position} to {end_position}...")
        return end_position
    else:
        return start_position