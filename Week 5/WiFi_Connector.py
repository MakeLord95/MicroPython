import time
import network
from machine import reset
from oled_utils import oled_setup

def connect_to_wifi(SSID, PASSWORD):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    while wlan.isconnected() == False:
        print("Waiting for connection...")
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError("Error while connecting to wifi")
    else:
        print("Connected to wifi")
    
    return wlan.ifconfig()


oled = oled_setup()

try:
    ssid = "KMD657_Group8"
    password = "viiskytkuus"
    ip = connect_to_wifi(ssid, password)
    oled.text(ip[0], 1, 1)
    oled.show()
except KeyboardInterrupt:
    reset()
    