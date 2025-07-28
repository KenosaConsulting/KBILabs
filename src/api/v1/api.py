from src.api.v1.endpoints import digital_gap
from fastapi import APIRouter
from .endpoints import companies

api_router = APIRouter()
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])


# Digital Gap Analyzer routes
api_router.include_router(
    digital_gap.router,
    prefix="/digital-gap",
    tags=["digital-gap"]
)
