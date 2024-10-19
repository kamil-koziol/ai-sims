from uuid import uuid4

import pytest
from fastapi import status

from api.tests.utils import create_sample_game


def test_create_interaction_success(client, game_data):
    game = create_sample_game(client)
    # Prepare interaction request payload
    agents = game_data["agents"]
    locations = game_data["locations"]

    interaction_request = {
        "game_id": game_data["id"],
        "initializing_agent": agents[0]["id"],
        "target_agent": agents[1]["id"],
        "surroundings": ["hello", "there"],
        "location": locations[0],  # Assuming the first location from game_data
    }

    # Create interaction
    response_interaction = client.post("/interaction/", json=interaction_request)

    # Asserts for interaction response
    assert response_interaction.status_code == status.HTTP_200_OK
    interaction_response = response_interaction.json()
    assert "status" in interaction_response
    assert isinstance(interaction_response["status"], bool)


def test_missing_game(client, game_data):
    # Create game
    response = client.post("/game/", json=game_data)
    assert response.status_code == status.HTTP_200_OK

    interaction_request = {
        "game_id": str(uuid4()),
        "initializing_agent": game_data["agents"][0]["id"],
        "target_agent": game_data["agents"][1]["id"],
        "surroundings": ["hello", "there"],
        "location": game_data["locations"][0],
    }

    response = client.post("/interaction/", json=interaction_request)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Game not found"


def test_missing_initializing_agent(client, game_data):
    # Create game
    response = client.post("/game/", json=game_data)
    assert response.status_code == status.HTTP_200_OK

    interaction_request = {
        "game_id": game_data["id"],
        "initializing_agent": str(uuid4()),
        "target_agent": game_data["agents"][1]["id"],
        "surroundings": ["hello", "there"],
        "location": game_data["locations"][0],
    }

    response = client.post("/interaction/", json=interaction_request)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Initializing agent not found"


def test_missing_target_agent(client, game_data):
    # Create game
    response = client.post("/game/", json=game_data)
    assert response.status_code == status.HTTP_200_OK

    interaction_request = {
        "game_id": game_data["id"],
        "initializing_agent": game_data["agents"][0]["id"],
        "target_agent": str(uuid4()),
        "surroundings": ["hello", "there"],
        "location": game_data["locations"][0],
    }

    response = client.post("/interaction/", json=interaction_request)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Target agent not found"
