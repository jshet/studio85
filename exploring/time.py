import PicoRobotics
import utime as time
import urequests
import WiFiTest

board = PicoRobotics.KitronikPicoRobotics()

json_date = "http://date.jsontest.com"

def get_h_and_m():
    r = urequests.get(json_date)
    print(r.status_code)
    rj = r.json()
    str_time = rj["time"]
    hour = str_time.split(":")[0]
    minute = str_time.split(":")[1]
    r.close()

    return hour, minute

try:
    WiFiTest.get_online()
    for i in range(10):
        hour, minute = get_h_and_m()
        print(hour, minute)
        int_h = int(hour)
        int_m = int(minute)
        board.step(1, "f", int_h, speed=250)
        time.sleep(1)
        board.step(2, "f", int_m, speed=250)
        time.sleep(60)
        
    WiFiTest.get_offline()

except Exception as Ex:
    WiFiTest.get_offline()
    print(Ex)