# Import libaries
from machine import Pin, I2C
import utime
import ssd1306


# Pins for OLED
OLED_SCL = 15
OLED_SDA = 14

# Initialize I2C to use OLED
i2c = I2C(1, scl=Pin(OLED_SCL), sda=Pin(OLED_SDA), freq=400000)
OLED_WIDTH = 128
OLED_HEIGHT = 64
oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

# Rotary coder Pins
C_LEFT = 10
C_RIGHT = 11

# Pins for the coder
p1 = Pin(C_LEFT, Pin.IN)
p2 = Pin(C_RIGHT, Pin.IN)


# Coder function
def decode(pin):
    global a0, b0, i
    # Read the pin values
    a = p1.value()
    b = p2.value()
    # Knob is turned left
    if a0 != a:
        i = i - 1
        a0 = a
    # Knob is turned right
    if b0 != b:
        i = i + 1
        b0 = b
    # Print the variable
    oled.fill(0)
    oled.text(str(i), 1, 1)
    oled.show()
    print(i)


# Activate interruptions
p1.irq(decode, Pin.IRQ_FALLING)
p2.irq(decode, Pin.IRQ_FALLING)

# Initialize global variables
a0, b0, i = 0, 0, 0

# Continue until stopped
while True:
    # Sleep 100 ms
    utime.sleep_ms(100)
