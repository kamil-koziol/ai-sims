import yaml
from fastapi import status
from fastapi.testclient import TestClient

from .utils import create_sample_game


def test_get_yaml_game(client: TestClient):
    game = create_sample_game(client)
    response = client.get(f"/games/{game.id}/yaml")
    assert response.status_code == status.HTTP_200_OK
    try:
        for _ in yaml.scan(response.text):
            pass  # Iterate through tokens to ensure no syntax errors
    except yaml.YAMLError as e:
        assert False, f"YAML is not well-formed: {e}"


def test_create_yaml_game(client: TestClient):
    game = create_sample_game(client)
    response = client.get(f"/games/{game.id}/yaml")
    assert response.status_code == status.HTTP_200_OK

    post_response = client.post(
        "/games/yaml",
        content=response.text,
        headers={"Content-Type": "application/yaml"},
    )

    assert post_response.status_code == status.HTTP_200_OK
    assert "game" in post_response.json()
