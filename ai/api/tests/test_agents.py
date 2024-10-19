from uuid import uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from api.routers.game import CreateAgentRequest, CreateAgentResponse
from api.tests.utils import create_sample_game


def test_add_agent(client: TestClient):
    game = create_sample_game(client)
    create_agent_request = CreateAgentRequest(
        name="John Smith",
        description="Very basic john",
        lifestyle="lifestyle",
        age=30,
    )
    response = client.post(
        f"/games/{game.id}/agents", json=create_agent_request.model_dump()
    )
    assert response.status_code == status.HTTP_200_OK

    resp: CreateAgentResponse = CreateAgentResponse.model_validate(response.json())
    assert resp.agent.name == create_agent_request.name
    assert resp.agent.description == create_agent_request.description
    assert resp.agent.lifestyle == create_agent_request.lifestyle
    assert resp.agent.id != None
