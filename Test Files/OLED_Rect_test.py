import time
from machine import Pin, PWM
from oled_utils import oled_setup


# LED Brightness controller
def brightness(led):
    global pct
    led.duty_u16(round((pct / 100) * 65534))
    
# Reset value
def reset(pin):
    global i, value, pct
    i, value, pct = 0, 0, 0
    
# Coder function
def decode(pin):
    global a0, b0, i, value, pct
    
    # Read the pin values
    a = p1.value()
    b = p2.value()
    
    # Knob is turned left
    if i > 0:
        if a0 != a:
            i = i - 1
            a0 = a
            
    # Knob is turned right 
    if i < 48:
        if b0 != b:
            i = i + 1
            b0 = b
        
    value = round((i / 48) * 108)
    pct = round((i / 48) * 100)
    
# LED pins
led_pins = [20, 21, 22]

# Create LEDs
leds = [PWM(Pin(pin)) for pin in led_pins]

# Turn all leds of at start
for led in leds:
    led.duty_u16(0)
        
# Setup rotary push button
rot_button = Pin(12, Pin.IN, Pin.PULL_UP)

# Pins for the coder
p1 = Pin(10, Pin.IN)
p2 = Pin(11, Pin.IN)

# Activate interruptions
p1.irq(decode, Pin.IRQ_FALLING)
p2.irq(decode, Pin.IRQ_FALLING)

# Create the interrupt for rotary button
rot_button.irq(handler=reset, trigger=Pin.IRQ_FALLING)

# Initialize global variables
a0, b0, i, pct, value, pwm_value = 0, 0, 0, 0, 0, 0

# Create OLED using custom library
oled = oled_setup()

while True:
    brightness(leds[0])
    
    oled.fill(0)
    oled.text("LED 1", 47, 17)
    oled.text(f"{pct}%", 47, 27)
    oled.rect(10, 47, 108, 5, 1)
    
    oled.fill_rect(10, 47, value, 5, 1)
    oled.show()
    
    time.sleep(1 / 75)