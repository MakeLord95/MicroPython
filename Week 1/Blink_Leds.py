import time
from machine import Pin


def switch_leds():
    for led in leds:
        led.on()
        time.sleep(1)
        led.off()

    leds_off()
    time.sleep(1)


def leds_off():
    for led in leds:
        led.off()


if __name__ == '__main__':
    led_pins = [22, 21, 20]
    leds = [Pin(pin, Pin.OUT) for pin in led_pins]

    while True:
        leds_off()
        switch_leds()
