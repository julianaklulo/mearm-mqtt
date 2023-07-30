"""
ESP32 Subscriber.

This script is responsible for receiving the joystick values
from the broker and controlling the servos.
"""
from umqtt.simple import MQTTClient

from robotic_arm_servo import RoboticArmServo


SERVER = "SERVER_ADDRESS"
PORT = 1883

BASE_PIN = 18
BASE_MIN = 0
BASE_MAX = 180

LEFT_PIN = 19
LEFT_MIN = 100
LEFT_MAX = 180

CLAW_PIN = 21
CLAW_MIN = 25
CLAW_MAX = 70

RIGHT_PIN = 22
RIGHT_MIN = 35
RIGHT_MAX = 180


base = RoboticArmServo(BASE_PIN, BASE_MIN, BASE_MAX, 10, "X", 0)
left = RoboticArmServo(LEFT_PIN, LEFT_MIN, LEFT_MAX, 10, "Y", 140)
claw = RoboticArmServo(CLAW_PIN, CLAW_MIN, CLAW_MAX, 5, "X", 25)
right = RoboticArmServo(RIGHT_PIN, RIGHT_MIN, RIGHT_MAX, 10, "Y", 90)


def control_servos(topic: str, data: bytes):
    parsed_data = data.decode("utf-8")
    print(parsed_data)

    base_dir, left_dir, claw_dir, right_dir = parsed_data.split(":")

    base.move(base_dir)
    left.move(left_dir)
    claw.move(claw_dir)
    right.move(right_dir)


client = MQTTClient("subscriber", SERVER, port=PORT, keepalive=30)
client.set_callback(control_servos)


while True:
    try:
        client.connect()
        client.subscribe(b"joysticks_data")
        client.wait_msg()
    except Exception:
        client.disconnect()
