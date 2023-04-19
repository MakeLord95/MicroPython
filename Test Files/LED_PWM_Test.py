from machine import Pin, PWM
import time


led = PWM(Pin(22))
x = 65534
while True:
    led.duty_u16(x)
    print(x)
    x += 1
    time.sleep(1)
    