from picamera import PiCamera
from datetime import datetime
import time 

camera = PiCamera()
time.sleep(2)

camera.resolution = (1920, 1080)

timestamp = datetime.now().isoformat()
save_as = "/home/pi/" + timestamp + "h.264"

camera.start_recording(save_as)
camera.wait_recording(8)
camera.stop_recording()