CENTER_ID = 0
LEFT_ID = 1
RIGHT_ID = 2
BACK_ID = 3
FAR_THRESHOLD = 0.9
CLOSE_THRESHOLD = 0.2


class DecisionMaker:
    def __init__(self, agent):
        self.agent = agent

    def decideNextMove(self):
        if self.isDeadEnd():
            self.agent.movement_controller.makeUTurn()
        elif self.isCrossroad():
            self.handleCrossroad()
        elif self.isRightTurn():
            self.agent.movement_controller.makeRightTurn()
        elif self.isLeftTurn():
            self.agent.movement_controller.makeLeftTurn()
        else:
            self.agent.movement_controller.moveForward()

    def isCrossroad(self):
        """Detect if the robot is at a crossroad (left and right are both open)."""
        left_dist = self.agent.distances[LEFT_ID]
        right_dist = self.agent.distances[RIGHT_ID]
        return left_dist > FAR_THRESHOLD and right_dist > FAR_THRESHOLD

    def isRightTurn(self):
        """Check if the robot should turn right."""
        right_dist = self.agent.distances[RIGHT_ID]
        return right_dist > FAR_THRESHOLD

    def isLeftTurn(self):
        """Check if the robot should turn left."""
        left_dist = self.agent.distances[LEFT_ID]
        return left_dist > FAR_THRESHOLD

    def isDeadEnd(self):
        """Check if the robot is at a dead end."""
        front_dist = self.agent.distances[CENTER_ID]
        return front_dist < CLOSE_THRESHOLD

    def handleCrossroad(self):
        """Handles decision-making at a crossroad."""
        self.agent.movement_controller.moveNoCorrection()
