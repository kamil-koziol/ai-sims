from typing import Annotated, Any, Dict, List
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel

from game.game import Game as GlobalGame
from game.game_manager import GameManager

from ..errors import GameExistsErr, GameNotFoundErr
from ..mappers import AgentMapper, GameMapper
from ..schemas import Agent, Game, Location
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
        raise GameExistsErr

    newGame: Game = Game(game_request.agents, game_request.locations)

    GameManager().add_game(
        game_id=game_request.id, game=GameMapper.request_to_game(game_request)
    )

    state.games[game_request.id] = newGame
    return {"id": game_request.id}


class CreateAgentRequest(BaseModel):
    name: str
    age: int
    description: str
    lifestyle: str


class CreateAgentResponse(BaseModel):
    agent: Agent


@router.post("/{game_id}/agents", response_model=CreateAgentResponse)
async def create_agent(
    game_id: Annotated[UUID, Path(title="Game id")],
    payload: CreateAgentRequest,
    state: State = Depends(get_state),
):
    if game_id not in state.games:
        raise GameNotFoundErr

    agent = Agent(
        id=uuid4(),
        name=payload.name,
        age=payload.age,
        description=payload.description,
        lifestyle=payload.lifestyle,
    )
    state.games[game_id].agents.append(agent)

    GameManager().games[game_id].add_agent(AgentMapper.request_to_agent(agent))

    return CreateAgentResponse(agent=agent)
