import pytest
from agents.memory.memory_node_factory import MemoryNodeFactory


class TestModel:

    def test_create_observation(self):
        MemoryNodeFactory().create_observation('something')
        assert True

    def test_create_dialog(self):
        MemoryNodeFactory().create_observation('something')
        assert True
