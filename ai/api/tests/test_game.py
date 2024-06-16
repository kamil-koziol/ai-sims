from fastapi import status

from api.tests.sample_game import game_data


def test_create_game(client, game_data):
    response = client.post("/game/", json=game_data)
    assert response.status_code == status.HTTP_200_OK
    assert "id" in response.json()
    assert response.json()["id"] == game_data["id"]


def test_create_existing_game(client, game_data):
    client.post("/game/", json=game_data)
    response = client.post("/game/", json=game_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Game already exists"
