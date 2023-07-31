from servo import Servo


class RoboticArmServo(Servo):
    """
    A class that represents a servo in a robotic arm.

    The servo movement is defined by a direction, that can be
    - Left
    - Right
    - Up
    - Down

    Each servo has an axis, which will determine the directions
    it can be moved to:
    - A servo with the axis X can be moved to the left or to the right.
    - A servo with the axis Y can be moved up or down.

    The servo will only move if the direction is valid.

    :param pin: The pin that the servo is connected to.
    :param angle_min: The minimum angle that the servo can be set to in the arm.
    :param angle_max: The maximum angle that the servo can be set to in the arm.
    :param increment: The increment that the servo will be moved by.
    :param axis: The axis that the servo will be moved on.
    :param angle: The initial angle that the servo will be set to.
    """

    def __init__(
        self,
        pin: int,
        angle_min: int,
        angle_max: int,
        increment: float,
        axis: str,
        angle: int = 90,
    ):
        super().__init__(pin, angle)
        self.angle_min = angle_min
        self.angle_max = angle_max
        self.increment = increment
        self.axis = axis

    def move(self, direction: str):
        """
        Move the servo in the specified direction.

        The servo will only move if the direction is within its axis.

        :param direction: The direction that the servo will be moved to.

        """
        if self.axis == "X":
            if direction == "Left" and self.angle > self.angle_min:
                self.sweep(self.angle - self.increment)
            elif direction == "Right" and self.angle < self.angle_max:
                self.sweep(self.angle + self.increment)

        elif self.axis == "Y":
            if direction == "Up" and self.angle < self.angle_max:
                self.sweep(self.angle + self.increment)
            elif direction == "Down" and self.angle > self.angle_min:
                self.sweep(self.angle - self.increment)
