from uuid import uuid4

import pytest
from fastapi import status

from api.tests.sample_game import game_data


def test_get_plan_success(client, game_data):
    # Create game
    response = client.post("/game/", json=game_data)
    assert response.status_code == status.HTTP_200_OK

    # Prepare plan request payload
    agents = game_data["agents"]
    locations = game_data["locations"]

    plan_request = {
        "game_id": game_data["id"],
        "agent_id": agents[0]["id"],
        "location": locations[0],  # Assuming the first location from game_data
    }

    response_plan = client.post("/plan/", json=plan_request)

    assert response_plan.status_code == status.HTTP_200_OK
    plan_response = response_plan.json()
    assert "plan" in plan_response
    assert len(plan_response["plan"]) > 0  # Ensure plan is not empty


def test_missing_game(client, game_data):
    # Create game
    response = client.post("/game/", json=game_data)
    assert response.status_code == status.HTTP_200_OK

    plan_request = {
        "game_id": str(uuid4()),
        "agent_id": game_data["agents"][0]["id"],
        "location": game_data["locations"][0],
    }

    response = client.post("/plan/", json=plan_request)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Game not found"


def test_agent_not_found(client, game_data):
    # Create game
    response = client.post("/game/", json=game_data)
    assert response.status_code == status.HTTP_200_OK

    plan_request = {
        "game_id": game_data["id"],
        "agent_id": str(uuid4()),
        "location": game_data["locations"][0],
    }

    response = client.post("/plan/", json=plan_request)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Agent not found"
