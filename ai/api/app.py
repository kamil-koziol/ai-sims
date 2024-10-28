from json import JSONEncoder
from uuid import UUID

import uvicorn
from fastapi import Depends, FastAPI

from .routers import game
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

    def run(self, host: str, port: int):
        uvicorn.run(self.app, host=host, port=port)
