from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List

from api.schemas import Location
from api.state import State, get_state
from game import GameManager
from ..mappers import LocationMapper

from memory import STM, STM_attributes


class PlanRequest(BaseModel):
    game_id: UUID
    agent_id: UUID
    location: Location


class PlanNode(BaseModel):
    location: str
    time: str


class PlanResponse(BaseModel):
    plan: List[PlanNode]


router = APIRouter()


@router.post("/", response_model=PlanResponse)
async def get_plan(
    plan_request: PlanRequest, state: State = Depends(get_state)
):
    game = state.games.get(plan_request.game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    agent = game.get_agent(plan_request.agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent_stm_params: STM_attributes = STM_attributes(
        id=agent.id,
        name=agent.name,
        description=agent.description,
        age=agent.age,
        curr_location=plan_request.location.name,
        lifestyle=agent.lifestyle,
    )

    agent_stm = STM(agent_stm_params)

    game = GameManager().games[plan_request.game_id]
    agent = game.get_agent(agent.id)

    # TODO: move location to agent schema
    agent.stm.curr_location = LocationMapper.request_to_location(
        plan_request.location
    )

    plan = agent.plan(game.locations)
    plan = [
        PlanNode(
            location=plan_node.location.name,
            time=plan_node.time.strftime("%m/%d/%Y, %H:%M:%S"),
        )
        for plan_node in plan
    ]
    return {"plan": plan}
