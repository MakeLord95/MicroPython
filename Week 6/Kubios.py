import time
import ujson
import network
from machine import Pin
import urequests as requests
from oled_utils import oled_setup

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

oled = oled_setup()
led = Pin("LED", Pin.OUT)
ssid = "KMD657_Group_8"
password = "viiskytkuus"
ip = connect_to_wifi(ssid, password)
print(ip[0])

TOKEN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/oauth2/token"
CLIENT_ID = "3pjgjdmamlj759te85icf0lucv"
CLIENT_SECRET = "111fqsli1eo7mejcrlffbklvftcnfl4keoadrdv1o45vt9pndlef"

APIKEY = "pbZRUi49X48I56oL1Lq8y8NDjq6rPfzX3AQeNo3a"
LOGIN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/login"
REDIRECT_URI = "https://analysis.kubioscloud.com/v1/portal/login"

response = requests.post(
    url=TOKEN_URL,
    data='grant_type=client_credentials&client_id={}'.format(CLIENT_ID),
    headers={'Content-Type': 'application/x-www-form-urlencoded'},
    auth=(CLIENT_ID, CLIENT_SECRET))


# print(response.text)
response = response.json()  # Parse JSON response into a python dictionary
access_token = response["access_token"]  # Parse access token out of the response dictionary
intervals = [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 756, 820, 812, 800]  # Interval data to be sent to KubiosCloud

data_set = {
    "type": "RRI",
    "data": intervals,
    "analysis":{
        "type": "readiness"
        }
    }

# Make the readiness analysis with the given data
response = requests.post(
    url="https://analysis.kubioscloud.com/v2/analytics/analyze",
    headers={"Authorization": "Bearer {}".format(access_token),
             # use access token to access your KubiosCloud analysis session
             "X-Api-Key": APIKEY},
    json=data_set)  # dataset will be automatically converted to JSON by the urequests library
response = response.json()
print(response)

oled.fill(0)

oled.text(f"PNS Index:", 1, 11)
oled.text(f"{response["analysis"]["pns_index"]}", 8, 21)

oled.text(f"SNS Index:", 1, 41)
oled.text(f"{response["analysis"]["sns_index"]}", 8, 51)

oled.show()