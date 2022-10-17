from picamera import PiCamera
from gpiozero import Button
from time import sleep

button = Button(2)

camera = PiCamera()

camera.resolution = (1920,1080)

camera.start_preview()
sleep(2)

camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.stop_preview()
camera.awb_gains = g

camera.start_preview()

frame = 10

while True:
	try:
		button.wait_for_press()
		camera.capture('/home/computer/kids/v/animation/motorcycle_repairs/frame%03d.jpg' % frame)
		frame += 1
	except KeyboardInterrupt:
		camera.stop_preview()
		break
