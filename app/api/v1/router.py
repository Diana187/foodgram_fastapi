from fastapi import APIRouter

from app.api.v1.routes import ping

router = APIRouter()
router.include_router(ping.router)
