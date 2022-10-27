from machine import RTC



rtc = RTC()

print(rtc.datetime())

hr = rtc.datetime()[4]
mn = rtc.datetime()[5]
sec = rtc.datetime()[6]

print(f"{hr=}, {mn=}, {sec=}")