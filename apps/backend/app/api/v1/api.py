from fastapi import APIRouter
from .endpoints import auth, chat, health, websocket

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(health.router, tags=["health"])
api_router.include_router(websocket.router, tags=["websocket"])
