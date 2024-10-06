class AgentState:
    def execute(self, agent):
        raise NotImplementedError()


class RunState(AgentState):
    def execute(self, agent):
        if agent.measures.visitingLed:
            agent.state = WaitState()
        if agent.measures.ground == 0:
            agent.setVisitingLed(True)
        agent.wander()


class WaitState(AgentState):
    def execute(self, agent):
        agent.setReturningLed(True)
        if agent.measures.visitingLed:
            agent.setVisitingLed(False)
        if agent.measures.returningLed:
            agent.state = ReturnState()
        agent.driveMotors(0.0, 0.0)


class ReturnState(AgentState):
    def execute(self, agent):
        if agent.measures.visitingLed:
            agent.setVisitingLed(False)
        if agent.measures.returningLed:
            agent.setReturningLed(False)
        agent.wander()


class StopState(AgentState):
    def execute(self, agent):
        pass
