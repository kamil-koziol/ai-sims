from fastapi import status
from fastapi.testclient import TestClient

from api.routers.game import CreateGameResponse
from api.schemas import Game

from .sample_game import game_data


def create_sample_game(client: TestClient) -> Game:
    response = client.post("/games", json=game_data())
    assert response.status_code == status.HTTP_200_OK
    create_game_response = CreateGameResponse.model_validate(response.json())
    return create_game_response.game
