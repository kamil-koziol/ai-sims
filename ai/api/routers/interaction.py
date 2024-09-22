import random
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from game import GameManager
from ..mappers import LocationMapper
from object_types import Objects

from memory.stm import STM, STM_attributes
from api.schemas import Location
from api.state import State, get_state

class InteractionRequest(BaseModel):
    game_id: UUID
    initializing_agent: UUID
    target_agent: UUID
    surroundings: List[str]
    location: Location


class InteractionResponse(BaseModel):
    status: bool


router = APIRouter()


@router.post("/", response_model=InteractionResponse)
async def create_interaction(
    interaction_request: InteractionRequest, state: State = Depends(get_state)
):

    game = state.games.get(interaction_request.game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    initializing_agent = game.get_agent(interaction_request.initializing_agent)
    if initializing_agent is None:
        raise HTTPException(status_code=404, detail="Initializing agent not found")

    target_agent = game.get_agent(interaction_request.target_agent)
    if target_agent is None:
        raise HTTPException(status_code=404, detail="Target agent not found")

    initializing_agent_stm_params: STM_attributes = STM_attributes(
        id=initializing_agent.id,
        name=initializing_agent.name,
        description=initializing_agent.description,
        age=initializing_agent.age,
        curr_location=interaction_request.location.name,
        lifestyle=initializing_agent.lifestyle,
    )

    initializing_agent_stm = STM(initializing_agent_stm_params)

    target_agent_stm_params: STM_attributes = STM_attributes(
        id=target_agent.id,
        name=target_agent.name,
        description=target_agent.description,
        age=target_agent.age,
        curr_location=interaction_request.location.name,
        lifestyle=target_agent.lifestyle,
    )


    game = GameManager().games[interaction_request.game_id]
    initializing_agent = game.get_agent(initializing_agent.id)
    target_agent = game.get_agent(target_agent.id)

    #TODO: move location to agent schema
    target_agent.stm.curr_location = LocationMapper.request_to_location(interaction_request.location)
    initializing_agent.stm.curr_location = LocationMapper.request_to_location(interaction_request.location)

    status = initializing_agent.should_converse([(Objects.AGENT, target_agent)]) is not None
    return {"status": status}
