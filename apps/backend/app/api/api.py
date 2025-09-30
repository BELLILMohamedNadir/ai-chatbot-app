from fastapi import APIRouter
from .v1.api import api_router as api_v1_router

api_router = APIRouter()

# Include v1 API routes (no prefix, already set in main.py)
api_router.include_router(api_v1_router)
