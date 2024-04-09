"""
Модуль с зависимостями для FastAPI.
"""

import json

from fastapi import HTTPException, status, Request
from app.core import settings
from app.database import Database, new_session


async def get_db():
    session = await new_session()
    try:
        yield Database(session)
    finally:
        await session.close()



# async def get_user(request: Request) -> dict:
#     try:
#         return {
#             "id": request.headers["x-v2-user-id"],
#             "telegram_id": request.headers["x-v2-user-tgid"],
#             "staff": request.headers["x-v2-user-is-staff"]
#         }
#     except KeyError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="User not transferred"
#         )
