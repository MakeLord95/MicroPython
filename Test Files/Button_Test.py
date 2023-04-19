from machine import Pin
import time


def switch_leds():
    for led in leds:
        led.on()
        time.sleep(0.25)
        led.off()

        if button.value() != 0:
            break


def leds_off():
    for led in leds:
        led.off()


button = Pin(12, mode=Pin.IN, pull=Pin.PULL_UP)

while True:
    led_pins = [22, 21, 20]
    leds = [Pin(pin, Pin.OUT) for pin in led_pins]

    if button.value() == 0:
        switch_leds()

    else:
        leds_off()
