from unittest.mock import Mock

from agents.memory.memory_node_factory import MemoryNodeFactory
from llm_model.model_service import ModelService
from agents.agent import Agent
from agents.memory.stm import Action
from agents.actions.converse import (
    converse,
    generate_conversation,
    get_memories,
    generate_memory_on_conversation,
    insert_convo_into_mem_stream, ConversationVariables, MemoryOnConversationVariables,
)

def test_converse(mocker):
    # Mocking the dependent functions
    mocker.patch("agents.actions.converse.generate_conversation", return_value="Generated Conversation")
    mocker.patch("agents.actions.converse.generate_conversation_summary", return_value="Generated Summary")
    mocker.patch("agents.actions.converse.insert_convo_into_mem_stream")

    # Mocking Agents
    init_agent = Mock()
    target_agent = Mock()
    init_agent.stm.action = Action.NOTHING
    target_agent.stm.action = Action.NOTHING

    # Calling the function to test
    converse(init_agent, target_agent)

    # Asserting that the dependent functions were called with the correct arguments
    agents.actions.converse.generate_conversation.assert_called_once_with(init_agent, target_agent)
    agents.actions.converse.generate_conversation_summary.assert_called_once_with(init_agent, target_agent, "Generated Conversation")
    agents.actions.converse.insert_convo_into_mem_stream.assert_called_with(init_agent, "Generated Conversation", "Generated Summary")
    agents.actions.converse.insert_convo_into_mem_stream.assert_called_with(target_agent, "Generated Conversation", "Generated Summary")

    # Asserting that the agent actions were updated
    assert init_agent.stm.action == Action.CONVERSING
    assert target_agent.stm.action == Action.CONVERSING

def test_generate_conversation(mocker):
    # Mocking the dependent functions
    mocker.patch("agents.actions.converse.get_memories", side_effect=["InitAgentMemories", "TargetAgentMemories"])
    mocker.patch.object(ModelService, 'generate_response', return_value="Generated Conversation")

    # Mocking Agents
    init_agent = Mock()
    init_agent.stm.name = "name1"
    init_agent.stm.description = "description1"
    init_agent.stm.action = Action.NOTHING
    init_agent.stm.location = "cafe"

    target_agent = Mock()
    target_agent.stm.name = "name2"
    target_agent.stm.description = "description2"
    target_agent.stm.action = Action.NOTHING

    prompt_variables = ConversationVariables(
        init_agent_name=init_agent.stm.name,
        target_agent_name=target_agent.stm.name,
        init_agent_description=init_agent.stm.description,
        target_agent_description=target_agent.stm.description,
        init_agent_action=init_agent.stm.action.value,
        target_agent_action=target_agent.stm.action.value,
        location=init_agent.stm.location,
        init_agent_memories="InitAgentMemories",
        target_agent_memories="TargetAgentMemories"
    )

    # Calling the function to test
    result = generate_conversation(init_agent, target_agent)

    # Asserting that the dependent functions were called with the correct arguments
    agents.actions.converse.get_memories.assert_called_with(init_agent, "TargetAgent")
    agents.actions.converse.get_memories.assert_called_with(target_agent, "InitAgent")
    ModelService.generate_response.assert_called_once_with(prompt_variables, "create_conversation.txt")

    # Asserting the result
    assert result == "Generated Conversation"

def test_get_memories(mocker):
    # Mocking the dependent function
    mocker.patch("agents.actions.converse.retrieve_relevant_memories", return_value=[
        Mock(attributes=Mock(description="Memory 1")),
        Mock(attributes=Mock(description="Memory 2"))
    ])

    # Mocking Agent
    agent = Mock()
    agent.stm.name = "name1"

    # Calling the function to test
    result = get_memories(agent, "Subject")

    # Asserting that the dependent function was called with the correct arguments
    agents.actions.converse.retrieve_relevant_memories.assert_called_once_with(agent, "Subject")

    # Asserting the result
    assert result == "Memory 1\nMemory 2"

def test_generate_memory_on_conversation(mocker):
    # Mocking the dependent function
    mocker.patch.object(ModelService, 'generate_response', return_value="Generated Memory")

    # Mocking Agent
    agent = Mock()
    agent.stm.name = "name1"

    # Calling the function to test
    result = generate_memory_on_conversation(agent, "Test Conversation")

    # Asserting that the dependent function was called with the correct arguments
    agents.actions.converse.ModelService.generate_response.assert_called_once_with(
        MemoryOnConversationVariables(conversation="Test Conversation", agent_name=agent.stm.name),
        "memo_on_convo.txt"
    )

    # Asserting the result
    assert result == "Generated Memory"

def test_insert_convo_into_mem_stream(mocker):
    # Mocking the dependent functions
    mocker.patch.object(MemoryNodeFactory, 'create_dialog', return_value=Mock())
    mocker.patch.object(MemoryNodeFactory, 'create_thought', return_value=Mock())
    mocker.patch.object(Agent.memory_stream, 'add_memory_node')
    mocker.patch("agents.actions.converse.generate_memory_on_conversation", return_value="Generated Memory")

    # Mocking Agent
    agent = Mock()
    agent.stm.name = "name1"

    # Calling the function to test
    insert_convo_into_mem_stream(agent, "Test Conversation", "Test Summary")

    # Asserting that the dependent functions were called with the correct arguments
    MemoryNodeFactory.create_dialog.assert_called_once_with("Test Summary", agent)
    MemoryNodeFactory.create_thought.assert_called_once_with("Generated Memory", agent)
    Agent.memory_stream.add_memory_node.assert_called_twice()
