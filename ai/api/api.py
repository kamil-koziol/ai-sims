from fastapi import Depends, FastAPI
from .routers import game, plan, conversation, interaction
from .state import get_state
import uvicorn

class Api:
    def __init__(self) -> None:
        self.app = FastAPI()

        self.app.include_router(game.router, prefix="/game", tags=["game"], dependencies=[Depends(get_state)])
        self.app.include_router(plan.router, prefix="/plan", tags=["plan"])
        self.app.include_router(conversation.router, prefix="/conversation", tags=["conversation"])
        self.app.include_router(interaction.router, prefix="/interaction", tags=["interaction"])

    def run(self) -> None:
        uvicorn.run(self.app, host="0.0.0.0", port=8000)