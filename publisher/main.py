"""
ESP32 Publisher.

This script is responsible for reading the joystick values
and sending them to the broker.
"""
from umqtt.simple import MQTTClient

from joystick import Joystick


SERVER = "SERVER_ADDRESS"
PORT = 1883

JOYSTICK_LEFT_PIN_X = 35
JOYSTICK_LEFT_PIN_Y = 34

JOYSTICK_RIGHT_PIN_X = 33
JOYSTICK_RIGHT_PIN_Y = 32

JOYSTICK_MIN = 10000
JOYSTICK_MAX = 60000


joystick_left = Joystick(
    JOYSTICK_LEFT_PIN_X, JOYSTICK_LEFT_PIN_Y, JOYSTICK_MIN, JOYSTICK_MAX
)
joystick_right = Joystick(
    JOYSTICK_RIGHT_PIN_X, JOYSTICK_RIGHT_PIN_Y, JOYSTICK_MIN, JOYSTICK_MAX
)

client = MQTTClient("publisher", SERVER, port=PORT, keepalive=30)

while True:
    joystick_left_state = joystick_left.get_state()
    joystick_right_state = joystick_right.get_state()

    data = f"{joystick_left_state}:{joystick_right_state}"
    print(data)

    client.connect()
    client.publish(b"joysticks_data", data)
    client.disconnect()
