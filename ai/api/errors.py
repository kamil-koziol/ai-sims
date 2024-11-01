from fastapi import HTTPException

GameNotFoundErr = HTTPException(status_code=404, detail="Game not found")
GameExistsErr = HTTPException(status_code=409, detail="Game already exist")

AgentNotFoundErr = HTTPException(status_code=404, detail="Agent not found")

InvalidDateFormatErr = HTTPException(
    status_code=422,
    detail="Invalid date format. Please refer to ISO8601. Example: 2018-08-18T00:00:00+1000",
)

UnprocessableEntityErr = HTTPException(
    status_code=422,
    detail="Did not pass validation.",
)
