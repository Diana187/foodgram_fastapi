from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session

router = APIRouter()


@router.get("/ping-db")
async def ping_db(session: AsyncSession = Depends(get_session)):
    return {"db": "ok"}
