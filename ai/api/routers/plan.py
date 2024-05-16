from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

class PlanRequest(BaseModel):
    agent_id: int

class PlanNode(BaseModel):
    action: str

class PlanResponse(BaseModel):
    plan: List[PlanNode]

router = APIRouter()

@router.post("/", response_model=PlanResponse)
async def get_plan(plan_request: PlanRequest):
    plan = [
        {"action": "move to location A"},
        {"action": "collect resource B"},
        {"action": "return to base"},
    ]
    return {"plan": plan}
