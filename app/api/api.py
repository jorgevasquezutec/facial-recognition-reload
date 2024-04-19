from fastapi import APIRouter

from app.api.facial.router import router as facial_router
from app.api.auth.router import router as auth_router
from app.config.constants import AUTH_PREFIX, FACIAL_PREFIX


api_router = APIRouter()
api_router.include_router(auth_router, prefix=AUTH_PREFIX, tags=["Auth"])
api_router.include_router(facial_router, prefix=FACIAL_PREFIX, tags=["Facial"])