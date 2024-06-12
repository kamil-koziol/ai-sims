from fastapi import Depends, FastAPI
from .routers import game, plan, conversation, interaction
from .state import get_state

app = FastAPI()

app.include_router(game.router, prefix="/game", tags=["game"], dependencies=[Depends(get_state)])
app.include_router(plan.router, prefix="/plan", tags=["plan"])
app.include_router(conversation.router, prefix="/conversation", tags=["conversation"])
app.include_router(interaction.router, prefix="/interaction", tags=["interaction"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

