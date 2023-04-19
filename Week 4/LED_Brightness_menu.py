import time
from machine import Pin, PWM
from oled_utils import oled_setup

# LED Brightness controller
def brightness(led):
    global pct
    led.duty_u16(int((pct / 100) * 65534))
    
def main_menu():
    global held
    global selected
    global menu_active
    global held
    
    oled.fill(0)
    
    oled.text("1. LED select", 14, 5)
    oled.text("2. Brightness", 14, 15)
    
    if selected == 1 or selected < 1:
        selected = 1
        oled.rect(13, 3, 106, 11, 1)
        
        if rot_btn.value() == 0 and not held:
            held = True
            menu_active = "LED_Sel"
        
        
    elif selected == 2 or selected > 2 and not held:
        
        selected = 2
        oled.rect(13, 13, 106, 11, 1)
        
        if rot_btn.value() == 0:
            held = True
            menu_active = "Bright"
        
    oled.show()


def led_select():
    global oled
    global menu_active
    global selected_led
    global selected
    global held
    
    oled.fill(0)
    oled.text("LED 1", 50, 5)
    oled.text("LED 2", 50, 15)
    oled.text("LED 3", 50, 25)
    
    if selected == 1 or selected < 1:
        selected = 1
        oled.rect(48, 3, 44, 11, 1)
        selected_led = 1
        
    elif selected == 2:
        oled.rect(48, 13, 44, 11, 1)
        selected_led = 2
        
    elif selected == 3 or selected > 3:
        selected = 3
        oled.rect(48, 23, 44, 11, 1)
        selected_led = 3
        
    oled.show()
    
    if rot_btn.value() == 0:
        held = True
        selected = 1
        menu_active = "Main"
        
# LED Brightness menu
def led_bright(led):
    global led_bright_list
    global selected_led
    global menu_active
    global selected
    global value
    global held
    global oled
    global pct
    
    brightness(led)
    
    oled.fill(0)
    oled.text(f"LED {selected_led}", 47, 17)
    oled.text(f"{pct}%", 47, 27)
    
    oled.rect(10, 47, 108, 5, 1)
    
    oled.fill_rect(10, 47, value, 5, 1)
    oled.show()
    
    if rot_btn.value() == 0:
        held = True
        selected = 2
        led_bright_list[selected_led - 1] = pct
        menu_active = "Main"
    
# Coder function
def decode(pin):
    global a0, b0, i
    global selected
    global pct
    global value
    global menu_active
    global led_bright_list
    global selected_led
    
    # Read the pin values
    a = left.value()
    b = right.value()
    
    # Knob is turned left
    if i > 0:
        if a0 != a:
            i = i - 1
            a0 = a
            
            selected -= 1
            
    # Knob is turned right 
    if i < 48:
        if b0 != b:
            i = i + 1
            b0 = b
            
            selected += 1
    # print(f"i: {i}, left: {left.value()}, right: {right.value()}, selected: {selected}")
    
    
# Pins for the rotary
left = Pin(10, Pin.IN)
right = Pin(11, Pin.IN)
rot_btn = Pin(12, Pin.IN, Pin.PULL_UP)

# Activate interruptions
left.irq(decode, Pin.IRQ_FALLING)
right.irq(decode, Pin.IRQ_FALLING)
# rot_btn.irq(rot_push, Pin.IRQ_FALLING)
    
# LED pins
led_pins = [22, 21, 20]

# Create LEDs
leds = [PWM(Pin(pin)) for pin in led_pins]

# Turn all leds of at start
for led in leds:
    led.duty_u16(0)

# Create OLED using custom library
oled = oled_setup()

i = 0
b0 = 0
a0 = 0
pct = 0
value = 0
held = False
selected = 0
selected_led = 1
menu_active = "Main"
led_bright_list = [0, 0, 0]

while True:
    if menu_active == "Main" and not held:
        main_menu()
    
    elif menu_active == "LED_Sel" and not held:
        led_select()
    
    elif menu_active == "Bright" and not held:
        led_bright(leds[selected_led - 1])
        
    if rot_btn.value() == 1:
        held = False
    
    # print(rot_btn.value())
    time.sleep(1 / 75)

