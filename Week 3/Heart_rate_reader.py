import time
import ssd1306
from machine import Pin, I2C, ADC


# Analog Pin values
A0 = 26
A1 = 27

# Pins for OLED
OLED_SCL = 15
OLED_SDA = 14

# Initialize I2C to use OLED
i2c = I2C(1, scl=Pin(OLED_SCL), sda=Pin(OLED_SDA), freq=400000)
OLED_WIDTH = 128
OLED_HEIGHT = 64
oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)


# Sampling frequency 50 Hz
fs = 50

# Gain and offset
gain = 2
offset = 46000

# Analog input and PWM control (LED)
adc = ADC(Pin(A0))
# Start coordinates for drawing a line
x0, y0 = 0, 0


def scale_signal(x):
    # Scale and offset are given in scale 2**16 = 65536
    # Then scale down to 2**6 = 64
    y = (gain * x - offset) // 1024
    # Limit low values to 0
    y = max(y, 0)
    # Limit high values to 64
    y = min(y, 64)
    return y

n = 0

while True:
    # Read the analog signal
    y_u16 = adc.read_u16()
    # Scale the signal down to scale from 0 to 64
    y = scale_signal(y_u16)
    # Take the modulus
    x = n % 129
    # Reset the display, when 128 pixels are used
    if x == 0:
        oled.fill(0)
        x0 = 0
    # Draw a line segment
    # Turn the y-axis upside down, as the origio (0,0) is in upper left corner
    oled.line(x0, 64 - y0, x, 64 - y, 1)
    oled.show()
    # Print the value (for debuggin)
    print(y)
    # Update line segment starting point
    x0 = x
    y0 = y
    
    n += 1
    
    # Sleep for sampling period
    time.sleep(1 / fs)

