"""
KBI Labs API Gateway - Scalable Architecture
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.api.routers import (
    companies, analytics, intelligence, 
    patents, market, portfolio, auth, health
)
from src.config.settings import get_settings
from src.integrations.registry import integration_registry
from src.utils.logging import setup_logging

settings = get_settings()
logger = setup_logging(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    logger.info("Starting KBI Labs API Gateway...")
    
    # Initialize all external API integrations
    await integration_registry.initialize_all()
    
    yield
    
    # Cleanup
    await integration_registry.close_all()
    logger.info("Shutting down KBI Labs API Gateway...")

app = FastAPI(
    title="KBI Labs Intelligence Platform",
    description="Scalable API Gateway for SMB Intelligence",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
API_V2_PREFIX = "/api/v2"

# Core business routers
app.include_router(companies.router, prefix=f"{API_V2_PREFIX}/companies", tags=["companies"])
app.include_router(analytics.router, prefix=f"{API_V2_PREFIX}/analytics", tags=["analytics"])
app.include_router(intelligence.router, prefix=f"{API_V2_PREFIX}/intelligence", tags=["intelligence"])

# External data routers
app.include_router(patents.router, prefix=f"{API_V2_PREFIX}/patents", tags=["patents"])
app.include_router(market.router, prefix=f"{API_V2_PREFIX}/market", tags=["market"])

# Platform features
app.include_router(portfolio.router, prefix=f"{API_V2_PREFIX}/portfolio", tags=["portfolio"])
app.include_router(auth.router, prefix=f"{API_V2_PREFIX}/auth", tags=["authentication"])
app.include_router(health.router, prefix="/health", tags=["health"])

@app.get("/")
async def root():
    return {
        "name": "KBI Labs Intelligence Platform",
        "version": "2.0.0",
        "documentation": "/api/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug
    )
