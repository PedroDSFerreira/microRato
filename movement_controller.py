class MovementController:
    def __init__(self, agent):
        self.agent = agent

    def moveForward(self):
        """Move the robot forward, adjusting speed based on sensor readings."""
        speed = self.calculateSpeed()
        self.agent.driveMotors(speed, speed)
        print("Moving forward with speed:", speed)

    def makeLeftTurn(self):
        """Make the robot turn left."""
        self.agent.driveMotors(-.5, .5)  # Example speeds for turning left
        print("Making a left turn")

    def makeRightTurn(self):
        """Make the robot turn right."""
        self.agent.driveMotors(.5, -.5)  # Example speeds for turning right
        print("Making a right turn")

    def makeUTurn(self):
        """Make the robot perform a U-turn."""
        self.agent.driveMotors(-1.0, 1.0)  # Example for a U-turn (turn in place)
        print("Making a U-turn")

    def stop(self):
        """Stop the robot."""
        self.agent.driveMotors(0.0, 0.0)
        print("Stopping the robot")

    def calculateSpeed(self):
        """
        Calculate the appropriate speed based on sensor readings.
        For simplicity, this implementation moves at a constant speed,
        but you could adjust it based on the environment.
        """
        return 1.0  # Return constant speed for now
