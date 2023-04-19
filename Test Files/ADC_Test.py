from machine import Pin, I2C, ADC, Timer, PWM
import ssd1306
import utime
import micropython
from led import Led
micropython.alloc_emergency_exception_buf(250)

def toggle_pin(tid):
    global adc_val
    
    adc_val = adc_count.read_u16()

# Pins for OLED
OLED_SCL = 15
OLED_SDA = 14

# Initialize I2C to use OLED
i2c = I2C(1, scl=Pin(OLED_SCL), sda=Pin(OLED_SDA), freq=400000)
OLED_WIDTH = 128
OLED_HEIGHT = 64
oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)


adc_count = ADC(26)


button = Pin(12, mode=Pin.IN, pull=Pin.PULL_UP)
pin_27 = Pin(27, mode=Pin.OUT)


adc_val = 0
adc_volts = 0


tmr = Timer(freq = 75, callback = toggle_pin)


while True:
    
    if button.value() == 1:
        pin_27.value(1)
        
    elif button.value() == 0:
        pin_27.value(0)
    
    adc_volts = (adc_val/65534)*3.3
    """
    oled.fill(0)
    
    oled.text(f"ADC 1: {adc_val}", 1, 1)
    
    oled.text(f"Pin 27: {pin_27.value()}", 1, 11)
    
    oled.text(f"ADC 1 V: {adc_volts:.2f}", 1, 21)
    
    oled.show()
    
    print("ADC Count: " + str(adc_val))
    print("ADC volts: " + str(adc_volts))
    """
    utime.sleep(0.025)