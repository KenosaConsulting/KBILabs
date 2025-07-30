"""Health Check Router"""
from fastapi import APIRouter
from src.utils.health_checker import HealthChecker

router = APIRouter()
health_checker = HealthChecker()

@router.get("/")
async def health_check():
    """Basic health check"""
    return await health_checker.check_health()

@router.get("/detailed")
async def detailed_health():
    """Detailed health check including all dependencies"""
    return await health_checker.detailed_check()
