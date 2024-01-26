from unittest.mock import Mock
from agents.memory import MemoryNodeFactory


class TestModel:
    def test_create_observation(self):
        MemoryNodeFactory().create_observation('something', Mock())
        assert True

    def test_create_dialog(self):
        MemoryNodeFactory().create_observation('something', Mock())
        assert True

    def test_create_thought(self):
        MemoryNodeFactory().create_thought('something', Mock())
        assert True
