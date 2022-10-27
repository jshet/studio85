import PicoRobotics
import utime as time

board = PicoRobotics.KitronikPicoRobotics()

class StepperMotor:
    def __init__(self):
        self.sequence = [["f","f"], ["r","f"], ["r","r"], ["f","r"]]
        self.coils = []
        
m1 = StepperMotor()
m1.coils = [1,2]

m2 = StepperMotor()
m2.coils = [3,4]

wife_sleeping = True

def motor_driver(motor, values):
    if wife_sleeping:
        print(motor.coils, values)
    else:
        board.motorOn(motor.coils[0], values[0],100)
        board.motorOn(motor.coils[1], values[1],100)

def step(motor, direction, delay=50):
    if direction == -1:
        motor.sequence.insert(0,motor.sequence.pop())
        motor_driver(motor, motor.sequence[-1])
    else:
        motor_driver(motor, motor.sequence[0])
        motor.sequence.append(motor.sequence.pop(0))
            
    time.sleep_ms(delay)
    
def test():
    try:        
        for i in range(5):
            step(m1, 1)
        for i in range(5):
            step(m2, -1)

    except Exception as ex:
        board.motorOff(1)
        board.motorOff(2)
        print(ex)

test()