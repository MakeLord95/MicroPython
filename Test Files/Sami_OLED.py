import time
from machine import Pin, I2C
import ssd1306

# Pins for OLED
OLED_SCL = 15
OLED_SDA = 14

# Initialize I2C to use OLED
i2c = I2C(1, scl=Pin(OLED_SCL), sda=Pin(OLED_SDA), freq=400000)
OLED_WIDTH = 128
OLED_HEIGHT = 64
oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

# Initialize buttons and LEDs
led1 = Pin(20, Pin.OUT)
led2 = Pin(21, Pin.OUT)
led3 = Pin(22, Pin.OUT)

sw0 = Pin(9, Pin.IN, Pin.PULL_UP)
sw1 = Pin(8, Pin.IN, Pin.PULL_UP)
sw2 = Pin(7, Pin.IN, Pin.PULL_UP)

encoder = Pin(12, Pin.IN, Pin.PULL_UP)

# Initialize LED states
led1_state = False
led2_state = False
led3_state = False

# Define callback function for encoder button interrupt
def encoder_button_pressed(pin):
    global led1_state, led2_state, led3_state
    led1_state = False
    led2_state = False
    led3_state = False

# Attach interrupt to encoder button pin
encoder.irq(trigger=Pin.IRQ_FALLING, handler=encoder_button_pressed)

# Main loop
while True:
    # Read button states and toggle corresponding LEDs
    if not sw0.value():
        led1_state = not led1_state
        led1.value(led1_state)
    if not sw1.value():
        led2_state = not led2_state
        led2.value(led2_state)
    if not sw2.value():
        led3_state = not led3_state
        led3.value(led3_state)

    # Update OLED display with LED states
    oled.fill(0)
    oled.text("LED1: " + str(led1_state), 0, 0)
    oled.text("LED2: " + str(led2_state), 0, 10)
    oled.text("LED3: " + str(led3_state), 0, 20)
    oled.show()
    # Delay to avoid excessive polling
    time.sleep(1)


