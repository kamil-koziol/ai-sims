from uuid import uuid4

from fastapi import status

from api.routers.game import CreateGameResponse, GetGameResponse
from api.tests.sample_game import game_data


def test_create_game(client, game_data):
    response = client.post("/game/", json=game_data)
    assert response.status_code == status.HTTP_200_OK

    create_game_response = CreateGameResponse.model_validate(response.json())

    assert len(create_game_response.game.agents) == len(game_data["agents"])
    assert create_game_response.game.agents[0].name == game_data["agents"][0]["name"]


def test_get_game_succeds_on_existing_game(client, game_data):
    response = client.post("/game/", json=game_data)
    assert response.status_code == status.HTTP_200_OK

    create_game_response = CreateGameResponse.model_validate(response.json())

    getResp = client.get("/game/" + str(create_game_response.game.id))
    assert getResp.status_code == status.HTTP_200_OK
    get_game_response = GetGameResponse.model_validate(response.json())
    assert create_game_response.game == get_game_response.game


def test_get_game_fails_on_missing_game(client, game_data):
    getResp = client.get("/game/" + str(uuid4()))
    assert getResp.status_code == status.HTTP_404_NOT_FOUND
