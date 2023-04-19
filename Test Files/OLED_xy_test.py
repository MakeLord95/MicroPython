from oled_utils import oled_setup

oled = oled_setup()

oled.fill(0)
oled.text("LED 1", 47, 17)
oled.show()

oled.rect(10, 20, 0, 5, 1)
oled.show()