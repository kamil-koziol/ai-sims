from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

class ConversationRequest(BaseModel):
    agent1_id: int
    agent2_id: int
    surroundings: List[str]

class ConversationResponse(BaseModel):
    agent1_conversation: List[str]
    agent2_conversation: List[str]

router = APIRouter()

@router.post("/", response_model=ConversationResponse)
async def create_conversation(conversation_request: ConversationRequest):
    # mocked conversation
    conversation_agent1 = ["Hello, how are you?", "What are you doing here?"]
    conversation_agent2 = ["I'm fine, thank you!", "Just exploring the area."]
    return {
        "agent1_conversation": conversation_agent1,
        "agent2_conversation": conversation_agent2,
    }
