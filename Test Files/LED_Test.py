from machine import Pin
from piotimer import Piotimer
import time

def toggle_led(tmr):
    led.toggle()

led = Pin(21, Pin.OUT)
tmr = Piotimer(freq=75, callback=toggle_led)

while True:
    time.sleep(0.1)