import math

from agent_state import ReturnState, RunState, StopState, WaitState
from croblink import CRobLinkAngs

CENTER_ID = 0
LEFT_ID = 1
RIGHT_ID = 2
BACK_ID = 3
THRESHOLD = 0.5


class Agent(CRobLinkAngs):
    def __init__(self, rob_name, rob_id, angles, host):
        super().__init__(rob_name, rob_id, angles, host)
        self.state = StopState()
        self.stopped_state = RunState()
        self.avg_distance = None

    def run(self):
        if self.status != 0:
            print("Connection refused or error")
            quit()

        self.readSensors()
        self.avg_distance = self.getAvgRealDistance()
        assert self.avg_distance is not None
        print("Average distance: ", self.avg_distance)

        while True:
            self.readSensors()

            print("Average distance: ", self.getAvgRealDistance())

            if self.measures.endLed:
                print(self.robName + " exiting")
                quit()

            if isinstance(self.state, StopState) and self.measures.start:
                self.state = self.stopped_state

            if not isinstance(self.state, StopState) and self.measures.stop:
                self.stopped_state = self.state
                self.state = StopState()

            self.state.execute(self)

    # def getError(self):
    #     # for each side, calculate the distance to the wall based on the angle
    #     # and get the diference between the reference value
    #     right_error = self.measures.irSensor[RIGHT_ID]

    def getRealDistance(self, idx, value):
        distance = value * math.sin(math.radians(self.angs[idx]))
        return distance if distance > THRESHOLD else None

    def getAvgRealDistance(self):
        right_distance = self.getRealDistance(
            RIGHT_ID, self.measures.irSensor[RIGHT_ID]
        )
        left_distance = self.getRealDistance(
            LEFT_ID, self.measures.irSensor[LEFT_ID]
        )

        return (
            (right_distance + left_distance) / 2
            if right_distance is not None and left_distance is not None
            else right_distance
            if right_distance is not None
            else left_distance
        )

    def wander(self):
        if (
            self.measures.irSensor[CENTER_ID] > THRESHOLD
            or self.measures.irSensor[LEFT_ID] > THRESHOLD
            or self.measures.irSensor[LEFT_ID] > THRESHOLD
            or self.measures.irSensor[LEFT_ID] > THRESHOLD
        ):
            print("Rotate left")
            self.driveMotors(-0.1, +0.1)
        elif self.measures.irSensor[LEFT_ID] > 2.7:
            print("Rotate slowly right")
            self.driveMotors(0.1, 0.0)
        elif self.measures.irSensor[RIGHT_ID] > 2.7:
            print("Rotate slowly left")
            self.driveMotors(0.0, 0.1)
        else:
            print("Go")
            self.driveMotors(0.1, 0.1)

    # In this map the center of cell (i,j), (i in 0..6, j in 0..13) is mapped to labMap[i*2][j*2].
    # to know if there is a wall on top of cell(i,j) (i in 0..5), check if the value of labMap[i*2+1][j*2] is space or not
    def setMap(self, labMap):
        self.labMap = labMap

    def printMap(self):
        for line in reversed(self.labMap):
            print("".join([str(i) for i in line]))
