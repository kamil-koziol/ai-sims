from uuid import uuid4

from fastapi import status

from api.errors import AgentNotFoundErr, GameNotFoundErr
from api.routers.game import CreateConversationRequest, CreateConversationResponse
from api.schemas import Game

from .utils import create_sample_game


def create_random_conversation_request(game: Game) -> CreateConversationRequest:
    initializing_agent = game.agents[0]
    target_agent = game.agents[1]

    req = CreateConversationRequest(
        initializing_agent_id=initializing_agent.id,
        target_agent_id=target_agent.id,
        surroundings=["some", "surroundings"],
        location=game.locations[0],
    )

    return req


def test_conversation_successful(client):
    game = create_sample_game(client)
    req = create_random_conversation_request(game)

    resp = client.post(f"/games/{str(game.id)}/conversations", json=req.model_dump())
    assert resp.status_code == status.HTTP_200_OK

    payload = CreateConversationResponse.model_validate(resp.json())
    assert len(payload.initialising_agent_conversation) != 0
    assert len(payload.target_agent_conversation) != 0


def test_missing_game(client):
    game = create_sample_game(client)
    req = create_random_conversation_request(game)
    response = client.post(
        f"/games/248bf7e0-b14b-48ce-b038-4313aea12f86/conversations",
        json=req.model_dump(),
    )

    assert response.status_code == GameNotFoundErr.status_code
    assert response.json()["detail"] == GameNotFoundErr.detail


def test_missing_initializing_agent(client):
    game = create_sample_game(client)
    req = create_random_conversation_request(game)
    req.initializing_agent_id = str(uuid4())

    response = client.post(f"/games/{game.id}/conversations", json=req.model_dump())

    assert response.status_code == AgentNotFoundErr.status_code
    assert response.json()["detail"] == AgentNotFoundErr.detail


def test_missing_target_agent(client):
    game = create_sample_game(client)
    req = create_random_conversation_request(game)
    req.target_agent_id = str(uuid4())

    response = client.post(f"/games/{game.id}/conversations", json=req.model_dump())

    assert response.status_code == AgentNotFoundErr.status_code
    assert response.json()["detail"] == AgentNotFoundErr.detail
