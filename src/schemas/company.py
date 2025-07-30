"""Company schemas for API validation"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class CompanyBase(BaseModel):
    uei: str
    name: str
    state: Optional[str] = None
    city: Optional[str] = None
    industry: Optional[str] = None

class Company(CompanyBase):
    """Basic company model"""
    pass

class CompanyDetail(CompanyBase):
    """Detailed company model with additional fields"""
    annual_revenue: Optional[float] = None
    employee_count: Optional[int] = None
    certifications: Optional[List[str]] = []
    metrics: Optional[Dict[str, Any]] = {}
    intelligence: Optional[Dict[str, Any]] = {}

class CompanyList(BaseModel):
    """Response model for company list"""
    companies: List[Company]
    total: int
    skip: int
    limit: int
