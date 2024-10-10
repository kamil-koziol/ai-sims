import os
import pytest
import yaml

from game import Game
from memory import MemoryStream, MemoryNodeFactory, STM_attributes, ImportanceEvaluator
from location import Location
from llm_model import ModelService
from uuid import UUID
from agents import Agent
from config.model import MOCK_MODELS


@pytest.fixture
def example_game(mocker):
    if MOCK_MODELS:
        mocker.patch.object(
            ImportanceEvaluator, 'calculate_importance_score', return_value=5
        )
        mocker.patch.object(
            ModelService, 'get_embeddings', return_value=[0.1, 0.2, 0.3]
        )

    stm1 = STM_attributes(
        UUID("{12345678-1234-5678-1234-567812345678}"),
        "John Smith",
        "John Smith is a dedicated father of two girls who balances his steady job "
        "at the post office with a passion for hiking in the great outdoors. "
        "Despite his busy schedule, he always finds time to explore nature's trails, "
        "instilling in his daughters a love for adventure and resilience.",
        27,
        Location("cafe"),
        "lazy",
    )
    agent1 = Agent(stm1)

    mem_stream = MemoryStream()

    chat = MemoryNodeFactory.create_chat("chat desc", agent1)
    thought = MemoryNodeFactory.create_thought("memory descr", agent1)
    observation = MemoryNodeFactory.create_observation("descript observ", agent1)

    mem_stream.add_memory_node(chat)
    mem_stream.add_memory_node(thought)
    mem_stream.add_memory_node(observation)

    agent1.memory_stream = mem_stream

    stm2 = STM_attributes(
        UUID("{12345678-1234-5678-1234-567812345679}"),
        "Emily Green",
        "Emily Green, a 25-year-old hairdresser with a flair for creativity, "
        "is single and finds joy in crafting delicious meals in her spare time. "
        "Her vibrant personality and culinary skills make her a beloved figure among "
        "friends and clients alike, often hosting dinner parties that showcase her "
        "talent and warmth.",
        27,
        Location("cafe"),
        "lazy",
    )
    agent2 = Agent(stm2)

    agents_list = [agent1, agent2]

    agents_dict = {}
    for agent in agents_list:
        agents_dict[agent.stm.id] = agent

    locations = [
        Location("cafe"),
        Location("park"),
        Location("office")
    ]

    game = Game(agents_dict, locations)
    return game


class TestGame:
    def test_save_to_yaml(self, example_game: Game):
        filename = "test_game1.yml"
        example_game.save_to_yaml(filename)

        curr_dir = os.path.dirname(__file__)
        storage_dir = os.path.join(curr_dir, "..", "storage")
        file_path = os.path.join(storage_dir, filename)
        assert os.path.exists(file_path)

    def test_load_from_yaml_file(self, example_game: Game):
        game = Game.load_from_yaml_file("test_game1.yml")

        loaded_name = game._agents[UUID("{12345678-1234-5678-1234-567812345679}")].stm.name
        original_name = example_game._agents[UUID("{12345678-1234-5678-1234-567812345679}")].stm.name
        assert loaded_name == original_name
        assert game.locations == example_game.locations

    def test_load_from_yaml_data(self, example_game: Game):
        parsed_yaml_game = yaml.dump(example_game, default_flow_style=False)

        game = Game.load_from_yaml_data(parsed_yaml_game)

        loaded_name = game._agents[UUID("{12345678-1234-5678-1234-567812345679}")].stm.name
        original_name = example_game._agents[UUID("{12345678-1234-5678-1234-567812345679}")].stm.name
        assert loaded_name == original_name
        assert game.locations == example_game.locations
