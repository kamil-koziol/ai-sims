from uuid import uuid4

from fastapi import status

from api.errors import AgentNotFoundErr, GameNotFoundErr
from api.routers.game import CreateInteractionRequest
from api.schemas import Game
from api.tests.utils import create_sample_game


def create_random_interaction_request(game: Game) -> CreateInteractionRequest:
    initializing_agent = game.agents[0]
    target_agent = game.agents[1]

    req = CreateInteractionRequest(
        initializing_agent_id=initializing_agent.id,
        target_agent_id=target_agent.id,
        surroundings=["some", "surroundings"],
        location=game.locations[0],
    )

    return req


def test_create_interaction_success(client):
    game = create_sample_game(client)
    req = create_random_interaction_request(game)

    response_interaction = client.post(
        f"/games/{game.id}/interactions", json=req.model_dump()
    )

    assert response_interaction.status_code == status.HTTP_200_OK
    interaction_response = response_interaction.json()
    assert "status" in interaction_response
    assert isinstance(interaction_response["status"], bool)


def test_missing_game(client):
    game = create_sample_game(client)
    req = create_random_interaction_request(game)

    response = client.post(
        f"/games/3ef0a584-2511-4696-9157-5ca6e09927cd/interactions",
        json=req.model_dump(),
    )
    assert response.status_code == GameNotFoundErr.status_code
    assert response.json()["detail"] == GameNotFoundErr.detail


def test_missing_initializing_agent(client):
    game = create_sample_game(client)
    req = create_random_interaction_request(game)
    req.initializing_agent_id = str(uuid4())

    response = client.post(
        f"/games/{game.id}/interactions",
        json=req.model_dump(),
    )

    assert response.status_code == AgentNotFoundErr.status_code
    assert response.json()["detail"] == AgentNotFoundErr.detail


def test_missing_target_agent(client):
    game = create_sample_game(client)
    req = create_random_interaction_request(game)
    req.target_agent_id = str(uuid4())

    response = client.post(
        f"/games/{game.id}/interactions",
        json=req.model_dump(),
    )

    assert response.status_code == AgentNotFoundErr.status_code
    assert response.json()["detail"] == AgentNotFoundErr.detail
