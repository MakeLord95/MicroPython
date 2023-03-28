import time
import ssd1306
from machine import Pin, I2C, PWM


# Coder function
def decode(pin):
    global a0, b0, i
    
    # Read the pin values
    a = p1.value()
    b = p2.value()
    
    
    if i >= 1:
        # Knob is turned left
        if a0 != a:
            i = i - 1
            a0 = a
        
    
    if i <= 49:
        # Knob is turned right
        if b0 != b:
            i = i + 1
            b0 = b
        # Print the variable
        
    value = i * 512 - 2
    
    if i <= 0:
        value = 0
    
    
    # leds[0].duty_u16(value)
    print(i)
    

if __name__ == '__main__':
    # LED pins
    led_pins = [20, 21, 22]
    
    # Create LEDs
    leds = [PWM(Pin(pin)) for pin in led_pins]
    
    # Pins for OLED
    OLED_SCL = 15
    OLED_SDA = 14

    # Initialize I2C to use OLED
    i2c = I2C(1, scl=Pin(OLED_SCL), sda=Pin(OLED_SDA), freq=400000)
    OLED_WIDTH = 128
    OLED_HEIGHT = 64
    oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)
    
    # Setup rotary button
    rot_button = Pin(12, Pin.IN, Pin.PULL_UP)
    
    # Rotary coder Pins
    C_LEFT = 10
    C_RIGHT = 11

    # Pins for the coder
    p1 = Pin(C_LEFT, Pin.IN)
    p2 = Pin(C_RIGHT, Pin.IN)

    # Activate interruptions
    p1.irq(decode, Pin.IRQ_FALLING)
    p2.irq(decode, Pin.IRQ_FALLING)

    # Initialize global variables
    a0, b0, i = 0, 0, 0
    
    # Main program loop
    while True:
        oled.fill(0)
        
        if rot_button.value() == 0:
            for led in leds:
                led.duty_u16(0)
        """
        if rot_button.value() == 0:
            oled.text('Button pressed', 1, 1)
        
        else:
            oled.text('Button not', 1, 1)
            oled.text('pressed!', 1, 11)
            
        oled.show()
        """
        time.sleep_ms(5)