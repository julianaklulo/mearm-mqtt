# MeArm MQTT
Control a MeArm robotic arm via MQTT using MicroPython.

## Context

### MeArm
MeArm is an open source and open hardware pocket sized robotic arm.

There are many versions available, the one used in this project is the
[MeArm V0.4](https://www.thingiverse.com/thing:360108m).

Any other version can be used as well.

### ESP32
ESP32 is a low-cost microcontroller with integrated WiFi and Bluetooth.

The version used in ths project is the 
[ESP32-DEVKIT-V1](https://circuits4you.com/2018/12/31/esp32-devkit-esp32-wroom-gpio-pinout/) with 30 pins.

It can be replaced by any other microcontroller that supports MicroPython and MQTT.

### MicroPython
MicroPython is a lean and efficient implementation of the Python 3 programming language that includes a small subset of the Python standard library and is optimised to run on microcontrollers and in constrained environments.

## Hardware
Using two ESP32 microcontrollers, it is possible to create a remote control for the MeArm via MQTT.

One ESP32 connected to 2 joysticks publishes the data to the MQTT broker, while the ESP32 connected to the MeArm
receives the joystick values and controls the servo motors accordingly.

### Components
- 1x MeArm robotic arm
    - 4 Servo motors
    - Power supply for the servos
- 2x ESP32-DEVKIT-V1 microcontroller
- 2x Analog joysticks

### Circuit Diagram

#### Publisher
<img src="https://github.com/julianaklulo/mearm-mqtt/assets/8601883/15f70e38-973c-4b68-a2c3-9ce04b0bfc51" width="500" height="600"></img>

#### Subscriber
<img src="https://github.com/julianaklulo/mearm-mqtt/assets/8601883/7a404b07-9b3a-4a4c-a511-4f9a49c8eb44" width="500" height="600"></img>

## Software
### Flash the MicroPython firmware
Follow the instructions on the [MicroPython ESP32 page](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html#esp32-intro) to flash the firmware.

### Setup a local MQTT broker
You can use a public MQTT broker, but it is recommended to use a local one for testing.

1. Download the [Mosquitto](https://mosquitto.org/download/) MQTT broker and install it on the machine you want to use
2. Enable the service and start it
```bash
sudo systemctl enable mosquitto.service
sudo systemctl start mosquitto.service
```
3. Check if the service is running correctly
```bash
sudo systemctl status mosquitto.service
```
4. Edit the configuration file (``/etc/mosquitto/mosquitto.conf``) to allow anonymous connections
```bash
echo "allow_anonymous true" >> /etc/mosquitto/mosquitto.conf
echo "listener 1883" >> /etc/mosquitto/mosquitto.conf
```
5. Restart the service
```bash
sudo systemctl restart mosquitto.service
```
6. Get the IP address of the machine and note it down
7. Test the connection to the broker by opening two terminals and running the following commands
```bash
mosquitto_sub -h <IP address> -t test
```
```bash
mosquitto_pub -h <IP address> -t test -m "Hello World"
```
8. If the message is received correctly, the broker is working correctly

### Configure the ESP32
1. Modify the boot.py to connect to your WiFi network. Change the following lines
```python
SSID = "your-wifi-ssid"
PASSWORD = "your-wifi-password"
```
2. Modify the main.py to connect to your MQTT broker
```python
SERVER = "your-mqtt-broker-ip"
PORT = 1883 # default MQTT port
```
3. Install the [ampy](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy) tool to manage the files on the ESP32
```bash
pip install adafruit-ampy
```
4. Connect both ESP32 to your computer via USB
5. Copy the files from the `publisher` folder to the ESP32 connected to the joysticks
```bash
ampy --port /dev/ttyUSB0 put publisher/boot.py
ampy --port /dev/ttyUSB0 put publisher/main.py
ampy --port /dev/ttyUSB0 put publisher/lib /lib
```
6. Copy the files from the `subscriber` folder to the ESP32 connected to the MeArm
```bash
ampy --port /dev/ttyUSB1 put subscriber/boot.py
ampy --port /dev/ttyUSB1 put subscriber/main.py
ampy --port /dev/ttyUSB1 put subscriber/lib/ /lib
```
7. Reboot both ESP32
```bash
ampy --port /dev/ttyUSB0 reset
ampy --port /dev/ttyUSB1 reset
```
8. Check if the ESP32 connected to the joysticks is publishing the joystick values
```bash
sudo screen /dev/ttyUSB0 115200
```
9. Check if the ESP32 connected to the MeArm is receiving the joystick values
```bash
sudo screen /dev/ttyUSB1 115200
```
10. Move the joysticks and check if the values are changing
11. If everything is working correctly, the MeArm should move accordingly

## Demo
https://github.com/julianaklulo/mearm-mqtt/assets/8601883/8447021f-89d7-4ae0-8fe1-f7fd2368b0d8
