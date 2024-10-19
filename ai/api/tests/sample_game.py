from uuid import uuid4


def game_data():
    return {
        "locations": [{"name": "coffee"}, {"name": "park"}],
        "agents": [
            {
                "id": str(uuid4()),
                "name": "John Smith",
                "age": 30,
                "description": "John's description",
                "lifestyle": "Active",
                "curr_location": "coffee",
            },
            {
                "id": str(uuid4()),
                "name": "Marry Jane",
                "age": 22,
                "description": "Merry's description",
                "lifestyle": "Lazy",
                "curr_location": "park",
            },
        ],
    }
