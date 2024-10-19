from fastapi import status

from api.routers.game import CreateGameResponse
from api.tests.sample_game import game_data


def test_create_game(client, game_data):
    response = client.post("/game/", json=game_data)
    assert response.status_code == status.HTTP_200_OK

    create_game_response = CreateGameResponse.model_validate(response.json())

    assert len(create_game_response.game.agents) == len(game_data["agents"])
    assert create_game_response.game.agents[0].name == game_data["agents"][0]["name"]
