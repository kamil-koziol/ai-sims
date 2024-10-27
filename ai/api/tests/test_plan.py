from fastapi import status

from api.errors import AgentNotFoundErr, GameNotFoundErr
from api.routers.game import CreatePlanRequest
from api.schemas import Game
from api.tests.utils import create_sample_game


def create_random_plan_request(game: Game) -> CreatePlanRequest:
    req = CreatePlanRequest(
        location=game.locations[0],
    )

    return req


def test_get_plan_success(client):
    game = create_sample_game(client)
    req = create_random_plan_request(game)
    agent_id = game.agents[0].id

    response = client.post(
        f"/games/{game.id}/agents/{agent_id}/plans", json=req.model_dump()
    )
    assert response.status_code == status.HTTP_200_OK

    plan_response = response.json()
    assert "plan" in plan_response
    assert len(plan_response["plan"]) > 0  # Ensure plan is not empty


def test_missing_game(client):
    game = create_sample_game(client)
    req = create_random_plan_request(game)
    agent_id = game.agents[0].id

    response = client.post(
        f"/games/f09c5272-1ae2-44fa-8aea-3b6699de6ea3/agents/{agent_id}/plans",
        json=req.model_dump(),
    )
    assert response.status_code == GameNotFoundErr.status_code
    assert response.json()["detail"] == GameNotFoundErr.detail


def test_agent_not_found(client):
    game = create_sample_game(client)
    req = create_random_plan_request(game)

    response = client.post(
        f"/games/{game.id}/agents/2fc13171-6a54-4690-b0a3-7d772e588238/plans",
        json=req.model_dump(),
    )
    assert response.status_code == AgentNotFoundErr.status_code
    assert response.json()["detail"] == AgentNotFoundErr.detail
