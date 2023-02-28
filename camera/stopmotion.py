from picamera import PiCamera
from gpiozero import Button
from time import sleep

button = Button(2)

camera = PiCamera()
camera.resolution = (1920,1080)
camera.rotation = 180

camera.preview_fullscreen=False 
camera.preview_window=(0, 38, 1920, 1080)

camera.start_preview()

camera.iso = 200
sleep(3)

camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

frame = 1

camera.annotate_text = f"{camera.resolution=}\n{camera.iso=}\n{camera.shutter_speed=}\n{camera.framerate=}\n{camera.exposure_mode=}\n{camera.awb_gains=}"

while True:
	try:
		button.wait_for_press()
		camera.annotate_text = ""
		camera.capture('/home/computer/frame%03d.jpg' % frame)
		frame += 1
		camera.annotate_text = f"{camera.resolution=}\n{camera.iso=}\n{camera.shutter_speed=}\n{camera.framerate=}\n{camera.exposure_mode=}\n{camera.awb_gains=}"
	except KeyboardInterrupt:
		camera.stop_preview()
		camera.stop_preview()
		break

camera.stop_preview()
