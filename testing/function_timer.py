import time

def timed_function(f, *args, **kwargs):
    myname = str(f).split(' ')[1]
    def new_func(*args, **kwargs):
        t = time.ticks_us()
        result = f(*args, **kwargs)
        delta = time.ticks_diff(time.ticks_us(), t)
        print('Function {} Time = {:6.3f}ms'.format(myname, delta/1000))
        return result
    return new_func

'''Put code below here, then decorate it and run to compare.'''

from machine import RTC

rtc = RTC()

def display_time_from_variable():
    moment = rtc.datetime()
    h = moment[4]
    m = moment[5]
    s = moment[6]
    return f'{h}:{m}:{s}'

def display_time_from_rtc():
    h = rtc.datetime()[4]
    m = rtc.datetime()[5]
    s = rtc.datetime()[6]
    return f'{h}:{m}:{s}'

@timed_function
def t_from_v(n=100):
    for i in range(n):
        t = display_time_from_variable()

@timed_function
def t_from_rtc(n=100):
    for i in range(n):
        t = display_time_from_rtc()

t_from_v(n=1)
t_from_rtc(n=1)