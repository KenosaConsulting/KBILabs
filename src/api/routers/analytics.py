"""Analytics API Router"""
from fastapi import APIRouter, Depends, Query
from typing import Optional, Dict
from src.services.analytics_service import AnalyticsService
from src.api.dependencies import get_current_user

router = APIRouter()
router_v1 = APIRouter()

analytics_service = AnalyticsService()

@router.get("/overview")
async def get_analytics_overview(
    state: Optional[str] = None,
    industry: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
):
    """Get analytics overview with optional filters"""
    return await analytics_service.get_overview(
        state=state,
        industry=industry,
        user_context=current_user
    )

@router.get("/trends")
async def get_trends(
    metric: str = Query(..., description="Metric to analyze"),
    period: str = Query("monthly", regex="^(daily|weekly|monthly|yearly)$"),
    current_user: Dict = Depends(get_current_user)
):
    """Get trend analysis for specific metrics"""
    return await analytics_service.get_trends(
        metric=metric,
        period=period,
        user_context=current_user
    )

@router.get("/benchmarks/{uei}")
async def get_company_benchmarks(
    uei: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get benchmarking data for a specific company"""
    return await analytics_service.get_benchmarks(uei, current_user)
