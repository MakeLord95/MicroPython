import time
import ssd1306
from machine import Pin, I2C


# Pins for OLED
OLED_SCL = 15
OLED_SDA = 14

# Initialize I2C to use OLED
i2c = I2C(1, scl=Pin(OLED_SCL), sda=Pin(OLED_SDA), freq=400000)
OLED_WIDTH = 128
OLED_HEIGHT = 64
oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)


while True:
    for x in range(128):
        for y in range(64):
            oled.fill_rect(0, 0, x, y, 1)
            oled.show()
                    
