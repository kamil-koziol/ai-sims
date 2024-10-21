from memory import STM_attributes, MemoryType
from agents import Agent
import pytest
from uuid import UUID
from location import Location


@pytest.fixture
def init_agent():
    stm = STM_attributes(
        UUID("{12345678-1234-5678-1234-567812345678}"),
        "John Smith",
        "John Smith is a dedicated father of two girls who balances his steady job "
        "at the post office with a passion for hiking in the great outdoors. "
        "Despite his busy schedule, he always finds time to explore nature's trails, "
        "instilling in his daughters a love for adventure and resilience.",
        27,
        Location("cafe"),
        "lazy",
    )
    agent = Agent(stm)
    return agent


class TestMemoryInjection:
    def test_memory_injection(self, init_agent: Agent):
        init_agent.inject_memory("John Smith went for hiking")
        init_agent.inject_memory("John Smith did a dinner.")
        init_agent.inject_memory("John Smith lost one of his daughters")

        assert len(init_agent.memory_stream.nodes) == 3
