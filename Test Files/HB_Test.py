from machine import ADC, Pin, I2C
import ssd1306
import time

# setup the Pulse Sensor reading pin
pulse=ADC(26)

max_samples = 1000
short_average=15
long_average=100
beat_threshold=200
finger_threshold=2000
history = []

# Pins for OLED
OLED_SCL = 15
OLED_SDA = 14

# Initialize I2C to use OLED
i2c = I2C(1, scl=Pin(OLED_SCL), sda=Pin(OLED_SDA), freq=400000)
OLED_WIDTH = 128
OLED_HEIGHT = 64
oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

def finger_detected():
    avg_1=sum(history[-short_average:])/short_average
    avg_2=sum(history[-long_average:])/long_average
    if avg_1-avg_2 > beat_threshold:
        oled.fill(0)
        oled.text("Heartbeat detected", 0, 0)
        oled.show()
        time.sleep_ms(500)
    else:
        oled.fill(0)
        oled.show()


n = 0

# main program
while True:
    x = n % 129
    value=pulse.read_u16()
    history.append(value)
    history = history[-max_samples:]

    # Scale the data to fit within the OLED display
    scaled_data = [int((val / 65535) * OLED_HEIGHT) for val in history]

    # Draw the graph on the OLED display
    if x == 0:
        oled.fill(0)
        
    
    for i in range(len(scaled_data) - 1):
        oled.line(i, OLED_HEIGHT - scaled_data[i], i + 1, OLED_HEIGHT - scaled_data[i + 1], 1)
    oled.show()

    if max(history)-min(history) < finger_threshold:
        finger_detected()