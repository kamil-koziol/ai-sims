from __future__ import annotations
from typing import List, TYPE_CHECKING
from dataclasses import dataclass
from llm_model import ModelService
from memory import PlanNode

if TYPE_CHECKING:
    from agents import Agent


def execute(agent: Agent):
    for plan in agent.stm.daily_plan:
        agent.move(plan.location)
