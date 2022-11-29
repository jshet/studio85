from machine import Pin
from time import sleep_us

# ===== Motor pins

motor_pins = [2, 3, 4, 5]
step_mode = "half" 	# options are half and full
m = []

for p in motor_pins:
    m.append(Pin(p, Pin.OUT))

# ===== Motor and gear settings

motor_step_angle = 1.8
full_step_mode = False
step_angle = motor_step_angle / 2 if not full_step_mode else motor_step_angle

tpi = 12
tpmm = tpi / 25.4
steps_per_rev = 360 / motor_step_angle

step_delay = 1250
move_delay = 100000

if full_step_mode:
    coil_steps = [[1,1,0,0],[0,1,1,0],[0,0,1,1],[1,0,0,1]]
else:
    coil_steps = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1]]

# ===== Unit calculations

steps_per_inch = tpi * steps_per_rev
steps_per_mm = tpmm * steps_per_rev
steps_per_deg = steps_per_rev / 360

def distance_to_steps(x):
    try:
        return float(x)
    except:
        x, unit = (float(x[:-2]), x[-2:].lower())
        if "in" in unit:
            steps = x * steps_per_inch
        elif "mm" in unit:
            steps = x * steps_per_mm
        elif "cm" in unit:
            steps = x * steps_per_mm * 10
        elif "dg" in unit:
            steps = x * steps_per_deg
        else:
            print("Unit of measure not recognized. Try 'in', 'inch', 'cm', 'mm' or leave blank for steps.")
        return steps

# ===== Motion control

def set_pins(motor, values):
    for i in range(4):
        motor[i].value(values[i])

def turn_off(motor):
    for p in motor:
        p.value(0)

def step(motor, direction):
    if direction == -1:
        coil_steps.reverse()
    # it using half step mode, do two half steps each time to maintain step counts
    if not full_step_mode:
        step_range = 2
    else:
        step_range = 1
    for i in range(step_range):
        pin_values = coil_steps[0]
        set_pins(motor, pin_values)
        coil_steps.append(coil_steps.pop(0))
        sleep_us(step_delay)
    if direction == -1:
        coil_steps.reverse()

def move(m, steps):
    if steps < 0:
        steps *= -1
        direction = -1
    else:
        direction = 1
    for i in range(steps):
        step(m, direction=direction)    
    turn_off(m)

# ===== Main

def main():
    try:
        while True:
            distance = input("-->")
            steps = distance_to_steps(distance)
            move(m, steps)
            print(f"{steps=}")
    except Exception as ex:
        turn_off(m)
        print(ex)

if __name__ == "__main__":
    main()
    