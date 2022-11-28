from machine import Pin
import time

m1 = Pin(2, Pin.OUT)
m2 = Pin(3, Pin.OUT)
m3= Pin(4, Pin.OUT)
m4 = Pin(5, Pin.OUT)

motor1 = [m1, m2, m3, m4]

motor_step_angle = 1.8
step_mode = "half"
step_angle = motor_step_angle / 2 if step_mode == "half" else motor_step_angle

tpi = 12
tpmm = tpi / 25.4

steps_per_inch = tpi * (step_angle * 360)
steps_per_mm = tpmm * (step_angle * 360)

delay = 1000

full_steps = [[1,1,0,0],[0,1,1,0],[0,0,1,1],[1,0,0,1]]
steps = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1]]

def send_it(motor, a, b, c, d):
    motor[0].value(a)
    motor[1].value(b)
    motor[2].value(c)
    motor[3].value(d)

def end_it():
    for x in motor1:
        x.value(0)

def move_cw(motor, step_list=steps, this_many=1, this_much=delay):
    for i in range(this_many):
        print(i)
        for move in step_list:
            send_it(motor, move[0],move[1],move[2],move[3])
            time.sleep_us(this_much)
    send_it(motor, 0,0,0,0)
    time.sleep(0.1)

def move_ccw(motor, step_list=steps, this_many=1, this_much=delay):
    step_list.reverse()
    print("moving ccw...")
    for i in range(this_many*-1):
        print(i)
        for move in step_list:
            send_it(motor, move[0],move[1],move[2],move[3])
            time.sleep_us(this_much)
    send_it(motor, 0,0,0,0)
    time.sleep(0.1)
    step_list.reverse()

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
            steps = x * steps_per_mm / 10
        else:
            print("Unit of measure not recognized. Try 'in', 'inch', 'cm', 'mm' or leave blank for steps.")
        return steps
    
def move(x, motor=motor1, direction=1, speed=2500):
    print(f"Preparing to move {x=}, {motor=}, {direction=}")
    if direction == 1:
        move_cw(motor, this_many=steps, this_much=speed)
    elif direction == -1:
        move_ccw(motor, this_many=steps, this_much=speed)
    else:
        print("Need to ask for directions?")

while True:
    distance = input("Ready >")
    steps = distance_to_steps(distance)
    direction = 1 if steps > 0 else -1
    move(steps, direction=direction, speed=1500)
    print(f"{steps=}, {direction=}")

end_it()