from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

from api.routers.game import CreateGameResponse, GetGameResponse

from .sample_game import game_data
from .utils import create_sample_game


def test_create_game(client: TestClient):
    game = game_data()
    response = client.post("/games/", json=game)
    assert response.status_code == status.HTTP_200_OK

    create_game_response = CreateGameResponse.model_validate(response.json())

    assert len(create_game_response.game.agents) == len(game["agents"])
    assert create_game_response.game.agents[0].id == game["agents"][0]["id"]
    assert create_game_response.game.agents[1].id == game["agents"][1]["id"]


def test_get_game_succeds_on_existing_game(client: TestClient):
    game = create_sample_game(client)

    response = client.get("/games/" + str(game.id))
    assert response.status_code == status.HTTP_200_OK
    get_game_response = GetGameResponse.model_validate(response.json())
    assert game == get_game_response.game


def test_get_game_fails_on_missing_game(client: TestClient):
    getResp = client.get("/games/" + str(uuid4()))
    assert getResp.status_code == status.HTTP_404_NOT_FOUND
