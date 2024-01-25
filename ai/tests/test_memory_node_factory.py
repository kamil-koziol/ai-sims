import pytest
from agents.memory.memory_node_factory import MemoryNodeFactory


class TestModel:

    def test_create_obeservation(self):
        MemoryNodeFactory().create_obeservation('something')
        assert True

    def test_create_dialog(self):
        MemoryNodeFactory().create_obeservation('something')
        assert True
