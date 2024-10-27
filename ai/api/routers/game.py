import os
import tempfile
from datetime import datetime
from typing import Annotated, Any, Dict, List
from uuid import UUID, uuid4

import yaml
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, ConfigDict, field_serializer

from api.mappers.location_mapper import LocationMapper
from game.game import Game as GlobalGame
from game.game_manager import GameManager
from memory.stm import STM, STM_attributes
from object_types import Objects
from utils import yaml_constructors

from ..errors import AgentNotFoundErr, GameExistsErr, GameNotFoundErr
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
        id=str(uuid4()), agents=game_request.agents, locations=game_request.locations
    )
    if game.id in state.games:
        raise GameExistsErr

    state.games[game.id] = game

    GameManager().add_game(
        game_id=UUID(game.id), game=GameMapper.api_game_to_game(game)
    )

    return CreateGameResponse(game=game)


@router.post(
    "/yaml",
    response_model=CreateGameResponse,
)
async def create_yaml_game(game_request: Request, state: State = Depends(get_state)):
    print("Hello")
    try:
        # Read and parse YAML from request body
        yaml_contents = await game_request.body()
        yaml_str = yaml_contents.decode("utf-8")
        print(yaml_str)
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail="Invalid YAML format")

    globalGame = GlobalGame.load_from_yaml_data(yaml_contents)
    globalGame.set_game_id(uuid4())

    game = GameMapper.game_to_api_game(globalGame)

    if game.id in state.games:
        raise GameExistsErr

    state.games[game.id] = game

    GameManager().add_game(game_id=UUID(game.id), game=globalGame)

    return CreateGameResponse(game=game)


class GetYamlGameResponse(BaseModel):
    yaml_contents: str


@router.get("/{game_id}/yaml", response_model=CreateGameResponse)
async def get_yaml_game(
    game_id: Annotated[str, Path(title="Game id")], state: State = Depends(get_state)
):
    if game_id not in state.games:
        raise GameNotFoundErr

    contents = GameManager().games[UUID(game_id)].to_yaml_string()
    return PlainTextResponse(content=contents, media_type="application/yaml")


class GetGameResponse(BaseModel):
    game: Game


@router.get("/{game_id}", response_model=CreateGameResponse)
async def get_game(
    game_id: Annotated[str, Path(title="Game id")], state: State = Depends(get_state)
):
    if game_id not in state.games:
        raise GameNotFoundErr

    game = state.games[game_id]
    return GetGameResponse(game=game)


class CreateAgentRequest(BaseModel):
    name: str
    age: int
    description: str
    lifestyle: str


class CreateAgentResponse(BaseModel):
    agent: Agent


@router.post("/{game_id}/agents", response_model=CreateAgentResponse)
async def create_agent(
    game_id: Annotated[str, Path(title="Game id")],
    payload: CreateAgentRequest,
    state: State = Depends(get_state),
):
    if game_id not in state.games:
        raise GameNotFoundErr

    agent = Agent(
        id=str(uuid4()),
        name=payload.name,
        age=payload.age,
        description=payload.description,
        lifestyle=payload.lifestyle,
    )
    state.games[game_id].agents.append(agent)

    GameManager().games[UUID(game_id)].add_agent(AgentMapper.request_to_agent(agent))
    return CreateAgentResponse(agent=agent)


def stm_attibutes_from_agent(a: Agent, location: Location) -> STM_attributes:
    return STM_attributes(
        id=UUID(a.id),
        name=a.name,
        description=a.description,
        age=a.age,
        curr_location=LocationMapper.request_to_location(location),
        lifestyle=a.lifestyle,
    )


class CreateConversationRequest(BaseModel):
    time: str
    initializing_agent_id: str
    target_agent_id: str
    surroundings: List[str]
    location: Location


class CreateConversationResponse(BaseModel):
    initialising_agent_conversation: List[str]
    target_agent_conversation: List[str]


@router.post("/{game_id}/conversations", response_model=CreateConversationResponse)
async def create_conversation(
    game_id: Annotated[str, Path(title="Game id")],
    conversation_request: CreateConversationRequest,
    state: State = Depends(get_state),
):
    game = state.games.get(game_id)
    if not game:
        raise GameNotFoundErr

    initializing_agent = game.get_agent(conversation_request.initializing_agent_id)
    target_agent = game.get_agent(conversation_request.target_agent_id)
    if initializing_agent is None or target_agent is None:
        raise AgentNotFoundErr

    game = GameManager().games[UUID(game_id)]
    assert game is not None

    initializing_agent = game.get_agent(
        UUID(conversation_request.initializing_agent_id)
    )
    assert initializing_agent is not None
    target_agent = game.get_agent(UUID(conversation_request.target_agent_id))
    assert target_agent is not None

    # TODO: move location to agent schema
    target_agent.stm.curr_location = LocationMapper.request_to_location(
        conversation_request.location
    )
    initializing_agent.stm.curr_location = LocationMapper.request_to_location(
        conversation_request.location
    )

    splitted_dialogs = initializing_agent.converse(target_agent=target_agent)

    conversation_agent1 = splitted_dialogs[
        UUID(conversation_request.initializing_agent_id)
    ]
    conversation_agent2 = splitted_dialogs[UUID(conversation_request.target_agent_id)]
    return CreateConversationResponse(
        initialising_agent_conversation=conversation_agent1,
        target_agent_conversation=conversation_agent2,
    )


class CreateInteractionRequest(BaseModel):
    initializing_agent_id: str
    target_agent_id: str
    surroundings: List[str]
    location: Location
    time: str


class CreateInteractionResponse(BaseModel):
    status: bool


@router.post("/{game_id}/interactions", response_model=CreateInteractionResponse)
async def create_interaction(
    game_id: Annotated[str, Path(title="Game id")],
    interaction_request: CreateInteractionRequest,
    state: State = Depends(get_state),
):
    game = state.games.get(game_id)
    if not game:
        raise GameNotFoundErr

    initializing_agent = game.get_agent(interaction_request.initializing_agent_id)
    target_agent = game.get_agent(interaction_request.target_agent_id)
    if initializing_agent is None or target_agent is None:
        raise AgentNotFoundErr

    game = GameManager().games[UUID(game_id)]
    initializing_agent = game.get_agent(UUID(initializing_agent.id))
    assert initializing_agent is not None
    target_agent = game.get_agent(UUID(target_agent.id))
    assert target_agent is not None

    target_agent.stm.curr_location = LocationMapper.request_to_location(
        interaction_request.location
    )
    initializing_agent.stm.curr_location = LocationMapper.request_to_location(
        interaction_request.location
    )

    status = (
        initializing_agent.should_converse([(Objects.AGENT, target_agent)]) is not None
    )
    return CreateInteractionResponse(status=status)


class PlanNode(BaseModel):
    location: str
    time: str


class CreatePlanRequest(BaseModel):
    time: str
    location: Location


class CreatePlanResponse(BaseModel):
    plan: List[PlanNode]


@router.post("/{game_id}/agents/{agent_id}/plans", response_model=CreatePlanResponse)
async def get_plan(
    game_id: Annotated[str, Path(title="Game id")],
    agent_id: Annotated[str, Path(title="Agent id")],
    plan_request: CreatePlanRequest,
    state: State = Depends(get_state),
):
    game = state.games.get(game_id)
    if not game:
        raise GameNotFoundErr

    agent = game.get_agent(agent_id)
    if agent is None:
        raise AgentNotFoundErr

    game = GameManager().games[UUID(game_id)]
    agent = game.get_agent(UUID(agent.id))
    assert agent is not None

    agent.stm.curr_location = LocationMapper.request_to_location(plan_request.location)

    plan = agent.plan(game.locations)
    plan = [
        PlanNode(
            location=plan_node.location.name,
            time=plan_node.time.isoformat(),
        )
        for plan_node in plan
    ]
    return CreatePlanResponse(plan=plan)
