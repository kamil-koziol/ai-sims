import uvicorn
from fastapi import Depends, FastAPI

from .routers import conversation, game, interaction, plan
from .state import get_state


class App:
    def __init__(self):
        self.app = FastAPI()

        self.app.include_router(
            game.router,
            prefix="/games",
            tags=["game"],
            dependencies=[Depends(get_state)],
        )
        self.app.include_router(
            plan.router,
            prefix="/plan",
            tags=["plan"],
            dependencies=[Depends(get_state)],
        )
        self.app.include_router(
            conversation.router,
            prefix="/conversation",
            tags=["conversation"],
            dependencies=[Depends(get_state)],
        )
        self.app.include_router(
            interaction.router,
            prefix="/interaction",
            tags=["interaction"],
            dependencies=[Depends(get_state)],
        )

    def run(self, host: str, port: int):
        uvicorn.run(self.app, host=host, port=port)
