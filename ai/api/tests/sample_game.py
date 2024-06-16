from uuid import uuid4

import pytest


@pytest.fixture
def game_data():
    return {
        "id": str(uuid4()),
        "locations": [{"name": "Test Location"}, {"name": "Test location 2"}],
        "agents": [
            {
                "id": str(uuid4()),
                "name": "Agent1",
                "age": 30,
                "description": "A test agent",
                "lifestyle": "Active",
            },
            {
                "id": str(uuid4()),
                "name": "Agent2",
                "age": 20,
                "description": "A test agent 2",
                "lifestyle": "Funny",
            },
        ],
    }
