from __future__ import annotations
from typing import List, TYPE_CHECKING
from dataclasses import dataclass
from utils import WorldTime
from llm_model import ModelService
from datetime import datetime
from memory import PlanNode
from location import Location
import re

if TYPE_CHECKING:
    from agents import Agent

@dataclass
class DailyPlanVariables:
    """
    Variables for creating daily plan for places to go.
    """
    persona_short_description: str
    persona_life_style: str
    datetime_now: str
    persona_first_names: str
    list_of_places: str

def create_daily_plan(agent: Agent, list_of_places: List) -> List[PlanNode]:
    """
    Create list of places for agent to visit during the day.

    Args:
        agent (Agent): agent to create plan for.
        list_of_places (List): list of places that he can visit.
    """
    template_file = 'daily_planning_only_places.txt'

    daily_plan_variables = DailyPlanVariables(
        persona_short_description=agent.stm.get_short_description(),
        persona_life_style=agent.stm.life_style,
        datetime_now=WorldTime().current_time.strftime("%m/%d/%Y, %H:%M:%S"),
        persona_first_names=agent.stm.name,
        list_of_places=str(list_of_places).strip('[').strip(']')
    )

    daily_plan = ModelService().generate_text(daily_plan_variables, template_file)
    print(daily_plan)
    plan = _retrieve_plan(daily_plan, list_of_places)
    return plan

def _retrieve_plan(generated_text: str, list_of_places: List[Location]) -> List[PlanNode]:
    plan = []
    plan_split = generated_text.split('Plan for today:')[1]
    
    plan_points = plan_split.split('\n')

    for plan_point in plan_points:
        location = _retrieve_location(plan_point=plan_point, list_of_places=list_of_places)
        time = _retrieve_time(plan_point=plan_point)
        plan_node = PlanNode(
            location=location,
            time=time
        )
        if plan_node.location is not None and plan_node.time is not None:
            plan.append(plan_node)
    
    return plan
        

def _retrieve_location(plan_point: str, list_of_places: List[Location]) -> Location:
    location = None
    for place in list_of_places:
        if place.name in plan_point:
            location = place
            break
    return location

def _retrieve_time(plan_point: str) -> datetime:
    time_string = re.search("..:.. ..", plan_point)
    if time_string is None:
        return None
    time_string = time_string.group().upper().strip()
    time_object = datetime.strptime(time_string, '%I:%M %p')
    current_time = WorldTime().current_time
    return datetime(
        year=current_time.year,
        month=current_time.month,
        day=current_time.day,
        hour=time_object.hour,
        minute=time_object.minute,
        second=0
    )

