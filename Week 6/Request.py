import time
import network
from machine import Pin
import urequests as requests

def connect_to_wifi(SSID, PASSWORD):
    global led
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Waiting for connection", end='')
    while wlan.isconnected() == False:
        print(".", end='')
        
        led.toggle()
        time.sleep(1)

    if wlan.status() != 3:
        led.off()
        raise RuntimeError("Error while connecting to wifi")
    else:
        print("")
        print("Connected to wifi")
        led.on()
    
    return wlan.ifconfig()


led = Pin("LED", Pin.OUT)
ssid = "KMD657_Group_8"
password = "viiskytkuus"
ip = connect_to_wifi(ssid, password)
print(ip[0])

url = 'http://192.168.108.115:8000/'

response = requests.get(url)
print(response.text)
