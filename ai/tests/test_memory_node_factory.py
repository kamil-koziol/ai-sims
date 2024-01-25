import pytest # noqa
from agents.memory.memory_node_factory import MemoryNodeFactory


class TestModel:

    def test_create_obeservation(self):
        MemoryNodeFactory().create_obeservation('something')

    def test_create_dialog(self):
        MemoryNodeFactory().create_dialog('something')

    def test_create_thought(self):
        MemoryNodeFactory().create_thought('something')
