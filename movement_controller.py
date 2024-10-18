import math

SPEED = 0.1
SPEED_DIFF = 0.05
KP = 0.3


class MovementController:
    def __init__(self, agent):
        self.agent = agent

    def moveForward(self):
        """Move the robot forward, adjusting direction based on sensor readings."""
        error = self.agent.getDistError()
        self.agent.driveMotors(SPEED - KP * error, SPEED + KP * error)
        print("Moving forward")

    def makeLeftTurn(self):
        """Make the robot turn left."""
        self.agent.driveMotors(
            SPEED - SPEED_DIFF, SPEED + SPEED_DIFF
        )  # Example speeds for turning left
        print("Making a left turn")
        print("DONE")

    def makeRightTurn(self):
        """Make the robot turn right."""
        self.agent.driveMotors(
            SPEED + SPEED_DIFF, SPEED - SPEED_DIFF
        )  # Example speeds for turning right
        print("Making a right turn")
        print("DONE")

    def makeUTurn(self):
        """Make the robot perform a U-turn."""
        self.rotate(180)
        print("Making a U-turn")
        print("DONE")

    def moveNoCorrection(self):
        """Move the robot forward without any correction."""
        self.agent.driveMotors(SPEED, SPEED)
        print("Moving forward without correction")
        print("DONE")

    def stop(self):
        """Stop the robot."""
        self.agent.driveMotors(0.0, 0.0)
        print("Stopping the robot")

    def rotate(self, alpha):
        it = math.ceil(math.radians(alpha) / SPEED)

        for _ in range(it):
            self.agent.driveMotors(SPEED, -SPEED)
            self.agent.readSensors()
