"""Main FastAPI application module."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager

from app.api.wallet import router as wallet_router
from app.core.config import settings
from app.core.exceptions import AppException
from app.core.exception_handlers import (
    app_exception_handler,
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler
)
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    await init_db()
    yield
    pass


app = FastAPI(
    title=settings.app_name,
    description="A microservice for retrieving TRON wallet information including balance, bandwidth, and energy",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

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
