from uuid import uuid4

from fastapi import status

from api.tests.sample_game import game_data


def test_conversation_successfull(client, game_data):
    # create game
    response = client.post("/game/", json=game_data)

    # converse
    agents = game_data["agents"]
    locations = game_data["locations"]

    initializing_agent = agents[0]
    target_agent = agents[1]

    # Prepare conversation request payload
    conversation_request = {
        "game_id": game_data["id"],
        "initializing_agent": initializing_agent["id"],
        "target_agent": target_agent["id"],
        "surroundings": ["hello", "there"],
        "location": locations[0],  # Assuming the first location from game_data
    }

    # Initiate conversation
    response_conversation = client.post("/conversation/", json=conversation_request)

    # Asserts for conversation response
    assert response_conversation.status_code == status.HTTP_200_OK
    conversation_response = response_conversation.json()
    assert "agent1_conversation" in conversation_response
    assert "agent2_conversation" in conversation_response


def test_missing_game(client, game_data):
    # create game
    response = client.post("/game/", json=game_data)

    conversation_request = {
        "game_id": str(uuid4()),
        "initializing_agent": game_data["agents"][0]["id"],
        "target_agent": game_data["agents"][1]["id"],
        "surroundings": ["hello", "there"],
        "location": game_data["locations"][0],
    }

    response = client.post("/conversation/", json=conversation_request)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Game not found"


def test_missing_initializing_agent(client, game_data):
    # create game
    response = client.post("/game/", json=game_data)

    conversation_request = {
        "game_id": game_data["id"],
        "initializing_agent": str(uuid4()),
        "target_agent": game_data["agents"][1]["id"],
        "surroundings": ["hello", "there"],
        "location": game_data["locations"][0],
    }

    response = client.post("/conversation/", json=conversation_request)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Initializing agent not found"


def test_missing_target_agent(client, game_data):
    # create game
    response = client.post("/game/", json=game_data)

    conversation_request = {
        "game_id": game_data["id"],
        "initializing_agent": game_data["agents"][0]["id"],
        "target_agent": str(uuid4()),
        "surroundings": ["hello", "there"],
        "location": game_data["locations"][0],
    }

    response = client.post("/conversation/", json=conversation_request)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Target agent not found"
