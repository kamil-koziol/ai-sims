from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import List, Dict, Any
from ..schemas import Location, Agent, Game
from game.game import Game as GlobalGame
from game.game_manager import GameManager
from ..mappers import GameMapper, AgentMapper
from ..state import State, get_state


class GameRequest(BaseModel):
    id: UUID
    locations: List[Location]
    agents: List[Agent]

class GameResponse(BaseModel):
    id: UUID

router = APIRouter()

@router.post("/", response_model=GameResponse)
async def create_game(game_request: GameRequest, state: State = Depends(get_state)):

    if game_request.id in state.games:
        raise HTTPException(status_code=400, detail="Game already exists")
    
    newGame: Game = Game(game_request.agents, game_request.locations)

    GameManager().add_game(game_id=game_request.id, game=GameMapper.request_to_game(game_request))

    state.games[game_request.id] = newGame
    return {"id": game_request.id}

class AddAgentRequest(BaseModel):
    game_id: UUID
    agent: Agent

class AddAgentResponse(BaseModel):
    game_id: UUID
    agents: List[Agent]

@router.post("/add_agent", response_model=AddAgentResponse)
async def add_agent(add_agent_request: AddAgentRequest, state: State = Depends(get_state)):
    game_id = add_agent_request.game_id
    agent = add_agent_request.agent
    if game_id not in state.games:
        raise HTTPException(status_code=404, detail="Game not found")

    GameManager().games[game_id].add_agent(AgentMapper.request_to_agent(add_agent_request.agent))
    
    
    state.games[game_id].agents.append(agent)
    return {"game_id": game_id, "agents": state.games[game_id].agents}