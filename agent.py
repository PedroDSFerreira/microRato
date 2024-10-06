from agent_state import RunState, StopState, WaitState, ReturnState
from croblink import CRobLinkAngs


CENTER_ID = 0
LEFT_ID = 1
RIGHT_ID = 2
BACK_ID = 3

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

        while True:
            self.readSensors()

            if self.measures.endLed:
                print(self.robName + " exiting")
                quit()

            if not self.avg_distance:
                self.avg_distance = (self.measures.irSensor[LEFT_ID] + self.measures.irSensor[RIGHT_ID])/2
                print("Average distance: ", self.avg_distance)

            if isinstance(self.state, StopState) and self.measures.start:
                self.state = self.stopped_state

            if not isinstance(self.state, StopState) and self.measures.stop:
                self.stopped_state = self.state
                self.state = StopState()

            self.state.execute(self)

    def wander(self):
        if (
            self.measures.irSensor[CENTER_ID] > 5.0
            or self.measures.irSensor[LEFT_ID] > 5.0
            or self.measures.irSensor[RIGHT_ID] > 5.0
            or self.measures.irSensor[BACK_ID] > 5.0
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
