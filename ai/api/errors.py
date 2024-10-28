from fastapi import HTTPException

GameNotFoundErr = HTTPException(status_code=404, detail="Game not found")
GameExistsErr = HTTPException(status_code=409, detail="Game already exist")

AgentNotFoundErr = HTTPException(status_code=404, detail="Agent not found")
