from agent_state import RunState, StopState
from croblink import CRobLinkAngs
from decision_maker import DecisionMaker
from movement_controller import MovementController
from sensor_buffer import SensorBuffer

SW_DISTANCE = 0.4667  # distance from the side sensor to the wall


class Agent(CRobLinkAngs):
    def __init__(self, rob_name, rob_id, angles, host):
        super().__init__(rob_name, rob_id, angles, host)
        self.state = StopState()
        self.stopped_state = RunState()
        self.sensor_wall_distance = SW_DISTANCE
        self.distances = [-1.0, -1 - 0, -1.0, -1.0]
        self.sensor_buffer = SensorBuffer()
        self.decision_maker = DecisionMaker(self)
        self.movement_controller = MovementController(self)

    def readSensors(self):
        super().readSensors()

        for i in range(4):
            raw_value = self.measures.irSensor[i]
            raw_value = raw_value if raw_value != 0 else 0.0001

            if raw_value is not None:
                self.sensor_buffer.add_sample(i, raw_value)

        for i in range(4):
            self.distances[i] = self.sensor_buffer.get_parsed_value(i)

    def run(self):
        if self.status != 0:
            print("Connection refused or error")
            quit()

        while True:
            self.readSensors()
            print(self.distances)

            if self.measures.endLed:
                print(self.robName + " exiting")
                quit()
            if not isinstance(self.state, StopState) and self.measures.stop:
                self.stopped_state = self.state
                self.state = StopState()

            self.state.execute(self)

    # In this map the center of cell (i,j), (i in 0..6, j in 0..13) is mapped to labMap[i*2][j*2].
    # to know if there is a wall on top of cell(i,j) (i in 0..5), check if the value of labMap[i*2+1][j*2] is space or not
    def setMap(self, labMap):
        self.labMap = labMap

    def printMap(self):
        for line in reversed(self.labMap):
            print("".join([str(i) for i in line]))
