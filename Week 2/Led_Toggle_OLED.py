import time
import ssd1306
from machine import Pin, I2C


# Interrupt handler
def interrupt_handler():
    for led in leds:
        led.off()

    for x in button_held:
        button_held[x] = False


# Function to update OLED
def update_oled():
    oled.fill(0)
    oled.show()

    leds_status = ['ON' if led.value() == 1 else 'OFF' for led in leds]

    oled.text('LED1 Status:', 1, 1)
    oled.text(leds_status[0], 1, 11)

    oled.text('LED2 Status:', 1, 21)
    oled.text(leds_status[1], 1, 31)

    oled.text('LED3 Status:', 1, 41)
    oled.text(leds_status[2], 1, 51)

    oled.show()


if __name__ == '__main__':
    # Pins for OLED
    OLED_SCL = 15
    OLED_SDA = 14

    # Initialize I2C to use OLED
    i2c = I2C(1, scl=Pin(OLED_SCL), sda=Pin(OLED_SDA), freq=400000)
    OLED_WIDTH = 128
    OLED_HEIGHT = 64
    oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

    # Pins for protoboard LEDs
    led_pins = [22, 21, 20]

    # Create LEDs
    leds = [Pin(pin, Pin.OUT) for pin in led_pins]

    # Pins for protoboard buttons
    button_pins = [7, 8, 9]

    # Create buttons
    buttons = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in button_pins]

    # Create rotary button
    rotary_btn = Pin(12, Pin.IN, Pin.PULL_UP)

    # Create an array for button toggle function
    button_held = [False, False, False]

    rotary_btn.irq(handler=interrupt_handler, trigger=Pin.IRQ_FALLING)
    update_oled()

    while True:
        for i, button in enumerate(buttons):
            if button.value() == 0 and not button_held[i]:
                button_held[i] = True
                leds[i].toggle()
                update_oled()

            elif button.value() == 1 and button_held[i]:
                button_held[i] = False

        time.sleep(0.05)
