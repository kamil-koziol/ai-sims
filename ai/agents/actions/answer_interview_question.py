from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

from agents.actions.retrieve import get_string_memories
from llm_model import ModelService

if TYPE_CHECKING:
    from agents import Agent


@dataclass
class InterviewQuestionVariables:
    """
    Variables for answering an interview question.
    """

    agent_name: str
    description: str
    lifestyle: str
    age: str
    curr_location: str
    curr_time: str
    daily_plan: str
    memories: str
    question: str


def answer_interview_question(agent: Agent, question: str) -> str:
    prompt_template_file = "answer_interview_question.txt"
    relevant_memories = get_string_memories(agent, question)
    prompt_variables = InterviewQuestionVariables(
        agent_name=agent.stm.name,
        description=agent.stm.description,
        lifestyle=agent.stm.life_style,
        age=str(agent.stm.age),
        curr_location=agent.stm.curr_location.name,
        curr_time=agent.stm.get_curr_time_str(),
        daily_plan=agent.stm.get_daily_plan_str(),
        memories=relevant_memories,
        question=question
    )

    response = ModelService().generate_text(
        prompt_variables, prompt_template_file
    )
    return response