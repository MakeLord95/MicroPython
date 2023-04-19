import time
from machine import Pin


def toggle_pico_led():
    pico_led.on()
    time.sleep(0.01)
    pico_led.off()


if __name__ == '__main__':
    pico_led = Pin("LED", Pin.OUT)

    led_pins = [20, 21, 22]
    leds = [Pin(pin, Pin.OUT) for pin in led_pins]

    binary = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]

    while True:
        for inner_array in binary:
            print(inner_array)

            for i, num in enumerate(inner_array):
                if num == 0:
                    leds[i].off()

                else:
                    leds[i].on()

                toggle_pico_led()

            time.sleep(1)
