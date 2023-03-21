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

# Wait for a second
utime.sleep(1)

# Fill with light
oled.fill(1)
oled.show()

# Wait for a second
utime.sleep(1)

# Clear the display (off)
oled.fill(0)

# Repeat 10 times
for n in range(10):
    # Write text to OLED
    oled.text('Hardware project', 1, 1)
    oled.text('School of ICT', 1, 11)
    oled.text('Metropolia UAS', 1, 21)
    oled.text('3.12.2022', 1, 31)
    # oled.text('----------------', 1, 41)
    oled.text('123456789-123456', 1, 48)
    # Draw rectangles around the last numbers
    oled.rect(0, 41, 128, 23, 2)
    oled.rect(0, 42, 128, 21, 2)
    oled.show()
    # Wait for 2 seconds
    utime.sleep(2)
    # Clear the display
    oled.fill(0)
    oled.show()
    # Wait for 0.5 second
    utime.sleep(0.5)
