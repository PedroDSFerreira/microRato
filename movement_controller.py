import time

from agent import CENTER_ID, CLOSE_THRESHOLD, LEFT_ID

SPEED = 0.10
SPEED_TURN = 0.01
KP = 0.09
KD = 0.07


class MovementController:
    def __init__(self, agent):
        self.agent = agent

    def moveForward(self):
        """Move the robot forward, adjusting direction based on sensor readings."""
        current_error = self.agent.getDistError()
        current_time = time.time()
        dt = current_time - self.agent.prev_time

        if dt > 0:
            error_derivative = (current_error - self.agent.prev_error) / dt
        else:
            error_derivative = 0

        left_speed = SPEED - (KP * current_error + KD * error_derivative)
        right_speed = SPEED + (KP * current_error + KD * error_derivative)

        self.agent.driveMotors(left_speed, right_speed)

        self.agent.prev_error = current_error
        self.agent.prev_time = current_time

    def stop(self):
        """Stop the robot."""
        self.agent.driveMotors(0.0, 0.0)

    def findPath(self):
        """Go in circles until a path is found."""
        while self.agent.distances[CENTER_ID] < CLOSE_THRESHOLD:
            self.agent.driveMotors(0.05, -0.05)
            self.agent.readSensors()
        self.moveNoCorrection()

    def moveNoCorrection(self, it=13):
        """Move the robot forward without any correction."""
        for _ in range(it):
            self.agent.driveMotors(0.15, 0.15)
            self.agent.readSensors()

    def rotate180(self):
        for _ in range(11):
            self.agent.driveMotors(0.143, -0.143)
            self.agent.readSensors()

    def makeSideTurn(self, direction):
        for i in range(13):
            if direction == LEFT_ID:
                self.agent.driveMotors(
                    SPEED - SPEED_TURN - i * 0.01, SPEED + SPEED_TURN + i * 0.01
                )
            else:
                self.agent.driveMotors(
                    SPEED + SPEED_TURN + i * 0.01, SPEED - SPEED_TURN - i * 0.01
                )

            self.agent.readSensors()

        # self.stop()
        # self.agent.readSensors()
        # exit()
