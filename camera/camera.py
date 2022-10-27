from picamera import PiCamera
from time import sleep
import os
from motion import *

camera = PiCamera()
picture_directory = "pics"

def take_pictures(min_focus, max_focus):
    print(f"BTN_NORTH: {min_focus}, BTN_WEST: {max_focus}")
    with camera:
        camera.resolution = (1920,1080)
        camera.framerate = 30
        
        stack_num = 5
        stack_spacing = 5
        stack_size = round((max_focus - min_focus) / stack_spacing)
        stack_delay = 5

        print(f"stack_num: {stack_num}\nstack_spacing: {stack_spacing}\nstack_size: {stack_size}\nstack_delay: {stack_delay}")
        sleep(2)
        
        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = 'off'
        
        g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = g
        
        camera.start_preview()

        compensate_backlash("backward") # start by taking up the slack

        for stack in range(stack_num):
            for snap in range(stack_size):
                camera.capture(os.path.join(picture_directory, f'{stack:04}_{snap:02}.jpg'))
                forward(stack_spacing)
                print(f"snap {snap} of stack {stack}")
            backward(stack_size*stack_spacing)
            compensate_backlash("backward")
            print(f"stack {stack} completed")
            sleep(stack_delay)

        camera.stop_preview()
