from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.database import init_db
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Initialize application resources before serving requests."""
    logger.info("Starting Renewable Energy Agent System")
    init_db()
    logger.info("Database initialized")
    yield


# Create FastAPI app
app = FastAPI(
    title="Renewable Energy Agent System",
    description="Agentic AI decision-support platform for renewable energy and grid operations",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Renewable Energy Agent System",
        "version": "0.1.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "renewable-energy-agent",
        "environment": settings.environment
    }


# Import routers
from app.api.routes import alerts, anomalies, approvals, assets, battery, demand, energy, forecasts, monitoring, optimization, reports, weather, workflow

# Include routers
app.include_router(assets.router, prefix="/assets", tags=["assets"])
app.include_router(energy.router, prefix="/energy", tags=["energy"])
app.include_router(monitoring.router, prefix="/monitoring", tags=["monitoring"])
app.include_router(weather.router, prefix="/weather", tags=["weather"])
app.include_router(forecasts.router, prefix="/forecast", tags=["forecasts"])
app.include_router(demand.router, prefix="/demand", tags=["demand"])
app.include_router(battery.router, prefix="/battery", tags=["battery"])
app.include_router(anomalies.router, prefix="/anomalies", tags=["anomalies"])
app.include_router(optimization.router, prefix="/optimization", tags=["optimization"])
app.include_router(approvals.router, prefix="/approvals", tags=["approvals"])
app.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])
app.include_router(workflow.router, prefix="/workflow", tags=["workflow"])
