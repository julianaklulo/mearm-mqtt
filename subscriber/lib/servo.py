import machine
from time import sleep


class Servo:
    """
    A class that represents a servo motor that can turn 0-180 degrees.

    The servo is controlled by a PWM signal in the range 0-655535.

    Since each servo has its own operating range, the minimum and maximum duty
    cycle supported by the servo must be specified.

    :param pin: The pin that the servo is connected to.
    :param angle: The initial angle that the servo will be set to.
    :param duty_min: The minimum duty that the servo can be set to.
    :param duty_max: The maximum duty that the servo can be set to.
    """

    def __init__(
        self, pin: int, angle: int = 90, duty_min: int = 2000, duty_max: int = 7000
    ):
        self.pin = machine.Pin(pin)
        self.servo = machine.PWM(self.pin, freq=50)
        self.duty_min = duty_min
        self.duty_max = duty_max
        self.angle = angle
        self.set_angle(angle)

    def convert_angle_to_duty(self, angle: int) -> int:
        """
        Convert an angle to a duty cycle.

        Makes a linear conversion from angle to duty cycle.

        The conversion takes into consideration the minimum and maximum
        angle and duty cycle supported by the servo.

        :param angle: The angle to be converted.
        :returns: The duty cycle that corresponds to the specified angle.
        """
        angle_min = 0
        angle_max = 180
        angle_range = angle_max - angle_min
        duty_range = self.duty_max - self.duty_min

        return int(
            (((angle - angle_min) * duty_range) / angle_range) + self.duty_min
        )

    def sweep(self, new_angle: int, delay: float = 0.005):
        """
        Move the servo to the specified angle.

        The servo will move in steps, with a delay between each step.

        :param new_angle: The angle that the servo will be moved to.
        :param delay: The delay between each step of the movement.
        """
        step = -1 if new_angle < self.angle else 1

        for i in range(self.angle, new_angle, step):
            self.set_angle(i)
            sleep(delay)

        self.angle = new_angle

    def set_angle(self, angle: int):
        """
        Set the angle of the servo.

        The servo will be moved immediately to the specified angle.

        :param angle: The angle that the servo will be set to.
        """

        duty = self.convert_angle_to_duty(angle)
        self.servo.duty_u16(duty)

        self.angle = angle
