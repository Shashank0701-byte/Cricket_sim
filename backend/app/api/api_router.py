from fastapi import APIRouter
from app.api import matches, stats, simulate

api_router = APIRouter()
api_router.include_router(matches.router, prefix="/matches", tags=["matches"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])
api_router.include_router(simulate.router, prefix="/simulate", tags=["simulation"])
