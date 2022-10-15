from machine import Pin
import time

m1 = Pin(2, Pin.OUT)
m2 = Pin(3, Pin.OUT)
m3= Pin(4, Pin.OUT)
m4 = Pin(5, Pin.OUT)

motor1 = [m1, m2, m3, m4]

three_sixty = 513
how_far = three_sixty

delay = 1000

steps = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
   ]

half_steps = [
    [1,1,0,0],
    [0,1,1,0],
    [0,0,1,1],
    [1,0,0,1]
   ]

def send_it(motor, a, b, c, d):
    motor[0].value(a)
    motor[1].value(b)
    motor[2].value(c)
    motor[3].value(d)

def end_it():
    for x in motor1:
        x.value(0)

def move(motor, step_list=steps, this_many=three_sixty, this_much=delay):
    for i in range(this_many):
        for move in step_list:
            send_it(motor, move[0],move[1],move[2],move[3])
            time.sleep_us(this_much)
    send_it(motor, 0,0,0,0)
    time.sleep(0.25)

def move_back(motor, step_list=steps, this_many=three_sixty, this_much=delay):
    step_list.reverse()
    for i in range(this_many):
        for move in step_list:
            send_it(motor, move[0],move[1],move[2],move[3])
            time.sleep_us(this_much)
    send_it(motor, 0,0,0,0)
    time.sleep(0.25)
    step_list.reverse()
    


move(motor1, this_many=400, this_much=1100)
move_back(motor1, this_many=800, this_much=1100)
#move(motor1, this_many=200, this_much=1200)
#move(motor1, this_many=200, this_much=1000)
#move(motor1, this_many=200, this_much=800)

end_it()