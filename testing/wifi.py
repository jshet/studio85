import time
import network
import urequests as requests
import secrets

import gauges

ssid = secrets.SSID
password = secrets.PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])

while True:
    
    # Do things here, perhaps measure something using a sensor?
    
    # and then define the headers and the payloads
    headers = ""
    payload = ""
    
    # Then send it in a try/except block
    try:
        print("sending...")
        response = requests.post(destination_url, headers=headers, data=payload)
        print("sent (" + str(response.status_code) + "), status = " + str(wlan.status()) + ")")
        response.close()
    except:
        print("could not connect (status = " + str(wlan.status()) + ")")
        wlan.disconnect()
        wlan.connect(ssid, password)
        if wlan.status() == 3:
            print('connected')
        else:
            print('failed')
            
    time.sleep(5)
    