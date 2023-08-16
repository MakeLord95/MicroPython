import machine
import network
import socket
import urequests
import utime
import json

# Set your Wi-Fi credentials
SSID = "KMD657_Group8"
PASSWORD = "viiskytkuus"

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(ssid, password)

        while not wlan.isconnected():
            utime.sleep(1)

    print("Connected to Wi-Fi")
    print(wlan.ifconfig())

def create_server(port=80):
    addr = socket.getaddrinfo("0.0.0.0", port)[0][-1]
    server = socket.socket()
    server.bind(addr)
    server.listen(1)
    print("Server listening on", addr)
    return server

def serve_request(conn):
    request = conn.recv(1024).decode("utf-8")
    print("Request received:", request)

    # Sample JSON data
    data = {
        "message": "Hello from Raspberry Pi Pico!",
        "temperature": 25.5,
        "humidity": 60
    }

    response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
    response += json.dumps(data)

    conn.sendall(response)
    conn.close()

def main():
    connect_to_wifi(SSID, PASSWORD)
    server = create_server()

    while True:
        conn, addr = server.accept()
        print("Connection from", addr)
        serve_request(conn)

main()
