from constants import CENTER_ID, CLOSE_THRESHOLD, FAR_THRESHOLD, LEFT_ID, RIGHT_ID


class DecisionMaker:
    def __init__(self, agent):
        self.agent = agent

    def decideNextMove(self):
        """Decide the next move based on the sensor readings."""
        # if self.panicMode():
        #     print("Panic mode activated")
        # self.agent.movement_controller.findPath()
        if self.isDeadEnd():
            print("Dead end detected")
            self.agent.movement_controller.rotate180()
        elif self.isCrossroad():
            print("Crossroad detected")
            self.handleCrossroad()
        elif self.isOpenRight():
            print("Making a right turn")
            self.agent.movement_controller.makeSideTurn(RIGHT_ID)
        elif self.isOpenLeft():
            print("Making a left turn")
            self.agent.movement_controller.makeSideTurn(LEFT_ID)
        else:
            self.agent.movement_controller.moveForward()

    def panicMode(self):
        """Check if the robot is about to hit a wall"""
        return (
            self.agent.distances[CENTER_ID] < CLOSE_THRESHOLD
            or self.agent.distances[LEFT_ID] < CLOSE_THRESHOLD
            or self.agent.distances[RIGHT_ID] < CLOSE_THRESHOLD
        )

    def isCrossroad(self):
        """Detect if the robot is at a crossroad (left and right are both open)."""
        return self.isOpenLeft() and self.isOpenRight() and self.isOpenFront()

    def isOpenRight(self):
        """Check if the robot should turn right."""
        right_dist = self.agent.distances[RIGHT_ID]
        return right_dist > FAR_THRESHOLD

    def isOpenLeft(self):
        """Check if the robot should turn left."""
        left_dist = self.agent.distances[LEFT_ID]
        return left_dist > FAR_THRESHOLD

    def isOpenFront(self):
        """Check if the robot should move forward."""
        front_dist = self.agent.distances[CENTER_ID]
        return front_dist > FAR_THRESHOLD

    def isDeadEnd(self):
        """Check if the robot is at a dead end."""
        return (
            (not self.isOpenLeft())
            and (not self.isOpenLeft())
            and (not self.isOpenFront())
        )

    def handleCrossroad(self):
        """Handles decision-making at a crossroad."""
        self.agent.movement_controller.moveNoCorrection()
