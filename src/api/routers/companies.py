"""Companies API Router - Handles all company-related endpoints"""
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional, Dict, Any
from src.models.database import get_db_connection
from src.services.company_service import CompanyService
from src.api.dependencies import get_current_user
from src.schemas.company import Company, CompanyList, CompanyDetail

router = APIRouter()
router_v1 = APIRouter()  # Legacy support

# Initialize service
company_service = CompanyService()

@router.get("/", response_model=CompanyList)
async def list_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    state: Optional[str] = None,
    search: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
):
    """List companies with optional filtering"""
    return await company_service.list_companies(
        skip=skip,
        limit=limit,
        state=state,
        search=search,
        user_context=current_user
    )

@router.get("/{uei}", response_model=CompanyDetail)
async def get_company(
    uei: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get detailed company information"""
    company = await company_service.get_company(uei, user_context=current_user)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.post("/{uei}/enrich")
async def enrich_company(
    uei: str,
    current_user: Dict = Depends(get_current_user)
):
    """Trigger enrichment for a specific company"""
    return await company_service.enrich_company(uei, user_context=current_user)

# Legacy v1 endpoints
@router_v1.get("/")
async def list_companies_v1(skip: int = 0, limit: int = 100):
    """Legacy endpoint - will be deprecated"""
    return await company_service.list_companies_legacy(skip, limit)
