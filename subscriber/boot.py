"""
Connect to a WiFi network on boot.
"""
import network


SSID = "SSID"
PASSWORD = "PASSWORD"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():
    print("Connecting to network...")
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        pass
    print("Network configuration:", wlan.ifconfig())
