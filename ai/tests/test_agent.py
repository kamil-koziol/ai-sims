from agents import Agent
from agents.memory import STM_attributes, MemoryNodeFactory


class TestAgent:

    def test_save(self):
        stm_attributes = STM_attributes(
            name="John Smith",
            description="young student",
            age=22,
            curr_location="cafe",
            lifestyle="active"
        )
        agent = Agent(init_parameters=stm_attributes, save_file="agent1.txt")
        agent.memory_stream.add_memory_node(MemoryNodeFactory.create_thought("I need to go shopping", agent))

        agent.save()
        assert True

    def test_init_load(self):
        agent = Agent(load_file="agent1.txt")

        assert agent.memory_stream.nodes[0].attributes.description == "I need to go shopping"

    def test_plan(self):
        stm_attributes = STM_attributes(
            name="John Smith",
            description="young student",
            age=22,
            curr_location="cafe",
            lifestyle="active"
        )
        agent = Agent(init_parameters=stm_attributes, save_file="agent1.txt")
        agent.plan()
        assert len(agent.stm.daily_plan) > 0
