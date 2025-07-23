"""Main FastAPI application module."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.wallet import router as wallet_router
from app.core.config import settings
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    init_db()
    yield
    # Shutdown
    pass


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="A microservice for retrieving TRON wallet information including balance, bandwidth, and energy",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(wallet_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "TRON Wallet Service API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "network": settings.tron_network
    }
