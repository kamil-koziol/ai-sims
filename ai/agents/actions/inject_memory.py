from __future__ import annotations
from typing import TYPE_CHECKING
from memory import MemoryNodeFactory

if TYPE_CHECKING:
    from agents import Agent

def inject_memory(description: str, agent: Agent) -> None:
    memory_node = MemoryNodeFactory.create_injection(description, agent, "User")
    agent.memory_stream.add_memory_node(memory_node)
    agent.logger.info("Added memory node to memory stream:%s\n", str(memory_node))
