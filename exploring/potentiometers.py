from machine import ADC
from time import sleep

pot1 = ADC(28)
pot2 = ADC(27)
pot3 = ADC(26)

while True:
    print(f"{pot1.read_u16()}\t{pot2.read_u16()}\t{pot3.read_u16()}")
    sleep(0.1)
