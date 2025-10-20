from fastapi import APIRouter

from app.api.v1.routes.ping_db import router as ping_db_router

router = APIRouter()
router.include_router(ping_db_router)
