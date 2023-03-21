import time
from machine import Pin, PWM


def toggle_pico_led():
    pico_led.on()
    time.sleep(0.01)
    pico_led.off()
    print('blink')


def fade_on(led):
    value = 0

    toggle_pico_led()
    time.sleep(0.1)

    while value <= 4096:
        led.duty_u16(value)
        time.sleep_ms(15)

        value += 64


def fade_off(led):
    value = 4096

    toggle_pico_led()
    time.sleep(0.1)

    while value >= 0:
        led.duty_u16(value)
        time.sleep_ms(15)

        value -= 64


if __name__ == '__main__':
    pico_led = Pin("LED", Pin.OUT)

    led_pins = [22, 21, 20]
    leds = [PWM(Pin(pin)) for pin in led_pins]

    binary = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]

    num = 0

    while True:
        for j, inner_array in enumerate(binary):
            print(inner_array)
            print(j)

            if j == 0 and num >= 1:
                fade_off(leds[2])
                fade_off(leds[1])
                fade_off(leds[0])

                toggle_pico_led()
                time.sleep(1)

            elif num == 0:
                for i in leds:
                    i.duty_u16(0)

                toggle_pico_led()
                time.sleep(1)

            elif j == 1:
                fade_on(leds[0])

                time.sleep(1)

            elif j == 2:
                fade_off(leds[0])
                fade_on(leds[1])

                time.sleep(1)

            elif j == 3:
                fade_on(leds[0])

                time.sleep(1)

            elif j == 4:
                fade_off(leds[1])
                fade_off(leds[0])
                fade_on(leds[2])

                time.sleep(1)

            elif j == 5:
                fade_on(leds[0])

                time.sleep(1)

            elif j == 6:
                fade_off(leds[0])
                fade_on(leds[1])

                time.sleep(1)

            elif j == 7:
                fade_on(leds[0])

                time.sleep(1)

            num = num + 1
