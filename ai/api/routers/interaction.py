import random
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from schemas import Region

class InteractionRequest(BaseModel):
    agent_id: int
    surroundings: Dict[str, Any]
    position: Region

class InteractionResponse(BaseModel):
    status: bool

router = APIRouter()

@router.post("/", response_model=InteractionResponse)
async def create_interaction(interaction_request: InteractionRequest):
    status = True if random.random() > 0.5 else False
    return {"status": status}
