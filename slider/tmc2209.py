from machine import Pin
from time import sleep_us, sleep


enable_pin = Pin(0, Pin.OUT)
dir_pin = Pin(2, Pin.OUT)
step_pin = Pin(4, Pin.OUT)

delay = 100

def step(usteps,direction=1,delay=delay):
    print(delay)
    try:
        enable_pin.value(0)
        dir_pin.value(direction)
        for i in range(usteps):
            step_pin.value(1)
            sleep_us(delay)
            step_pin.value(0)
            sleep_us(delay)
        dir_pin.value(0)
        enable_pin.value(1)
        print("Done")
    except Exception as ex:
        enable_pin.value(1)
        dir_pin.value(0)
        step_pin.value(0)
        print(ex)

def up_down():
    for i in range(20):
        delay = 300 - (i*10)
        step(400,direction=0,delay=delay)

    sleep(1)

    for i in range(20):
        delay = 100 + (i*10)
        step(400,delay=delay)

inch = 20 * 200 * 8
mm = round((20 * 200 * 8) /25.4)
d = 10*mm
step(d,direction=0,delay=80)
