import time
import ssd1306
from machine import Pin, PWM, I2C


# LED Brightness controller
def brightness(led, pct):
    led.duty_u16(int((pct / 100) * 65534))


# Menu switching with rotary push
def menu_switch(pin):
    global led_bright_list
    global selected_led
    global menu_active
    global selected
    global value
    global held
    global leds
    global pct
    global i

    if menu_active == "LED_Sel" and not held:
        selected = 1
        value = led_bright_list[selected_led]
        pct = int((value / 108) * 100)
        brightness(leds[selected_led], pct)
        i = int((value / 108) * 48)
        menu_active = "Bright"

    elif menu_active == "Bright" and not held:
        i = 0
        selected = 1
        led_bright_list[selected_led] = value
        pct = 0
        value = 0
        menu_active = "LED_Sel"

    held = True


# LED Selection menu
def led_select():
    global selected_led
    global menu_active
    global selected
    global held
    global oled

    oled.fill(0)

    oled.text("LED 1", 50, 5)
    oled.text("LED 2", 50, 15)
    oled.text("LED 3", 50, 25)

    if selected == 1:
        oled.rect(48, 3, 44, 11, 1)
        selected_led = 0

    elif selected == 2:
        oled.rect(48, 13, 44, 11, 1)
        selected_led = 1

    elif selected == 3:
        oled.rect(48, 23, 44, 11, 1)
        selected_led = 2

    oled.show()


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

    brightness(led, pct)

    oled.fill(0)
    oled.text(f"LED {selected_led + 1}", 47, 17)
    oled.text(f"{pct}%", 50, 27)

    oled.rect(10, 47, 108, 5, 1)

    oled.fill_rect(10, 47, value, 5, 1)
    oled.show()


# Rotary decoder
def decoder(pin):
    global led_bright_list
    global right_value_0
    global left_value_0
    global selected_led
    global menu_active
    global selected
    global bright
    global value
    global pct
    global i

    # Read the pin values
    left_value = left.value()
    right_value = right.value()

    # Rotary is turned left
    if i > 0:
        if left_value_0 != left_value:
            i -= 1
            left_value_0 = left_value

            if menu_active == "LED_Sel":
                selected -= 1
                selected = max(selected, 1)
                selected = min(selected, 3)

            if menu_active == "Bright":
                value = int((i / 48) * 108)
                value = max(value, 0)
                value = min(value, 108)

                pct = int((value / 108) * 100)

    # Rotary is turned right
    if i < 48:
        if right_value_0 != right_value:
            i += 1
            right_value_0 = right_value

            if menu_active == "LED_Sel":
                selected += 1
                selected = max(selected, 1)
                selected = min(selected, 3)

            if menu_active == "Bright":
                value = int((i / 48) * 108)
                value = max(value, 0)
                value = min(value, 108)

                pct = int((value / 108) * 100)


# Pins for the rotary
left = Pin(10, Pin.IN)
right = Pin(11, Pin.IN)
rot_btn = Pin(12, Pin.IN, Pin.PULL_UP)

# Activate interruptions
left.irq(decoder, Pin.IRQ_FALLING)
right.irq(decoder, Pin.IRQ_FALLING)
rot_btn.irq(menu_switch, Pin.IRQ_FALLING)

# LED pins
led_pins = [22, 21, 20]

# Create LEDs
leds = [PWM(Pin(pin)) for pin in led_pins]

# Turn all leds of at start
for led in leds:
    led.duty_u16(0)

# Create OLED variable
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# A lot of required variables
i = 0
pct = 0
value = 0
bright = 0
held = False
selected = 1
selected_led = 0
left_value_0 = 0
right_value_0 = 0
menu_active = "LED_Sel"
led_bright_list = [0, 0, 0]

while True:
    if menu_active == "LED_Sel" and not held:
        led_select()

    elif menu_active == "Bright" and not held:
        led_bright(leds[selected_led])

    if rot_btn.value() == 1:
        held = False

    time.sleep(1 / 250)
