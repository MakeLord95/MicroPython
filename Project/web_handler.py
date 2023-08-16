import time
import json
import socket
import network
import urequests


# Connect to wifi
def wifi_connector(SSID, PASSWORD):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    while wlan.isconnected() == False:
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError("Error while connecting to wifi")
    else:
        print("Connected to the Wifi")
        return wlan.ifconfig()


# Upload data to kubios and return the response
def kubios_upload(data):
    TOKEN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/oauth2/token"
    CLIENT_ID = "3pjgjdmamlj759te85icf0lucv"
    CLIENT_SECRET = "111fqsli1eo7mejcrlffbklvftcnfl4keoadrdv1o45vt9pndlef"

    APIKEY = "pbZRUi49X48I56oL1Lq8y8NDjq6rPfzX3AQeNo3a"
    LOGIN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/login"
    REDIRECT_URI = "https://analysis.kubioscloud.com/v1/portal/login"

    response = urequests.post(
        url=TOKEN_URL,
        data='grant_type=client_credentials&client_id={}'.format(CLIENT_ID),
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        auth=(CLIENT_ID, CLIENT_SECRET))

    response = response.json()  # Parse JSON response into a python dictionary
    access_token = response["access_token"]  # Parse access token out of the response dictionary

    data_set = {
        "type": "RRI",
        "data": data,
        "analysis":{
            "type": "readiness"
            }
        }
    
    # Make the readiness analysis with the given data
    response = urequests.post(
        url="https://analysis.kubioscloud.com/v2/analytics/analyze",
        headers={"Authorization": "Bearer {}".format(access_token),
                 # use access token to access your KubiosCloud analysis session
                 "X-Api-Key": APIKEY},
        json=data_set)  # dataset will be automatically converted to JSON by the uurequests library
    response = response.json()
    
    return response
