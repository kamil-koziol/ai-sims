from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from api.schemas import Location
from api.state import State, get_state

from agents.memory.stm import STM, STM_attributes

class PlanRequest(BaseModel):
    game_id: UUID
    agent_id: UUID
    location: Location

class PlanNode(BaseModel):
    action: str

class PlanResponse(BaseModel):
    plan: List[PlanNode]

router = APIRouter()

@router.post("/", response_model=PlanResponse)
async def get_plan(plan_request: PlanRequest, state: State = Depends(get_state)):
    game = state.games.get(plan_request.game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    agent = game.get_agent(plan_request.agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent_stm_params: STM_attributes = STM_attributes(
        name=agent.name,
        description=agent.description,
        age=agent.age,
        curr_location=plan_request.location.name,
        lifestyle=agent.lifestyle,
    )

    agent_stm = STM(agent_stm_params)


    # TODO: Implement a plan generation
    plan = [
        {"action": "move to location A"},
        {"action": "collect resource B"},
        {"action": "return to base"},
    ]
    return {"plan": plan}
