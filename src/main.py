from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Create FastAPI application
app = FastAPI(
    title="KBI Labs Intelligence Platform",
    description="Comprehensive business intelligence platform for SMBs and investors",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"]
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to KBI Labs Intelligence Platform",
        "platform": "Multi-database intelligence system",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "KBI Labs API",
        "databases": ["PostgreSQL", "MongoDB", "Neo4j", "Redis"],
        "streaming": "Kafka"
    }

@app.get("/api/v1/alpha/status")
async def alpha_platform_status():
    return {
        "platform": "Alpha - Investment Intelligence",
        "status": "ready",
        "features": ["deal_discovery", "market_intelligence", "due_diligence"]
    }

@app.get("/api/v1/compass/status")
async def compass_platform_status():
    return {
        "platform": "Compass - SMB Intelligence", 
        "status": "ready",
        "features": ["benchmarking", "best_practices", "growth_planning"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
