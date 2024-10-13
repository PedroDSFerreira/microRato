class BaseState:
    def execute(self, agent):
        raise NotImplementedError()


class RunState(BaseState):
    def execute(self, agent):
        if agent.measures.visitingLed:
            agent.state = WaitState()
        if agent.measures.ground == 0:
            agent.setVisitingLed(True)
        agent.decision_maker.decideNextMove()


class WaitState(BaseState):
    def execute(self, agent):
        agent.setReturningLed(True)
        if agent.measures.visitingLed:
            agent.setVisitingLed(False)
        if agent.measures.returningLed:
            agent.state = ReturnState()
        agent.driveMotors(0.0, 0.0)


class ReturnState(BaseState):
    def execute(self, agent):
        if agent.measures.visitingLed:
            agent.setVisitingLed(False)
        if agent.measures.returningLed:
            agent.setReturningLed(False)

        agent.state = RunState()
        agent.state.execute(agent)


class StopState(BaseState):
    def execute(self, agent):
        if agent.measures.start:
            agent.state = agent.stopped_state
