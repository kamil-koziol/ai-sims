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


class CreateGameRequest(BaseModel):
    locations: List[Location]
    agents: List[Agent]


class CreateGameResponse(BaseModel):
    game: Game


router = APIRouter()


@router.post("/", response_model=CreateGameResponse)
async def create_game(
    game_request: CreateGameRequest, state: State = Depends(get_state)
):
    game: Game = Game(
        id=uuid4(), agents=game_request.agents, locations=game_request.locations
    )
    if game.id in state.games:
        raise GameExistsErr

    state.games[game.id] = game

    GameManager().add_game(game_id=game.id, game=GameMapper.api_game_to_game(game))

    return CreateGameResponse(game=game)


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
