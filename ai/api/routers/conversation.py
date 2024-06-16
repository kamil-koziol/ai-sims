from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict

from api.schemas import Location
from api.state import State, get_state

from agents.memory.stm import STM, STM_attributes

class ConversationRequest(BaseModel):
    game_id: UUID
    initializing_agent: UUID
    target_agent: UUID
    surroundings: List[str]
    location: Location

class ConversationResponse(BaseModel):
    agent1_conversation: List[str]
    agent2_conversation: List[str]

router = APIRouter()

@router.post("/", response_model=ConversationResponse)
async def create_conversation(conversation_request: ConversationRequest, state: State = Depends(get_state)):
    game = state.games.get(conversation_request.game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    initializing_agent = game.get_agent(conversation_request.initializing_agent)
    if initializing_agent is None:
        raise HTTPException(status_code=404, detail="Initializing agent not found")
    
    target_agent = game.get_agent(conversation_request.target_agent)
    if target_agent is None:
        raise HTTPException(status_code=404, detail="Target agent not found")
    

    initializing_agent_stm_params: STM_attributes = STM_attributes(
        id=initializing_agent.id,
        name=initializing_agent.name,
        description=initializing_agent.description,
        age=initializing_agent.age,
        curr_location=conversation_request.location.name,
        lifestyle=initializing_agent.lifestyle,
    )

    initializing_agent_stm = STM(initializing_agent_stm_params)


    target_agent_stm_params: STM_attributes = STM_attributes(
        id = target_agent.id,
        name=target_agent.name,
        description=target_agent.description,
        age=target_agent.age,
        curr_location=conversation_request.location.name,
        lifestyle=target_agent.lifestyle,
    )

    target_agent_stm = STM(target_agent_stm_params)

    # TODO: implement conversation logic
    # mocked conversation
    conversation_agent1 = ["Hello, how are you?", "What are you doing here?"]
    conversation_agent2 = ["I'm fine, thank you!", "Just exploring the area."]
    return {
        "agent1_conversation": conversation_agent1,
        "agent2_conversation": conversation_agent2,
    }
