from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.core.config import settings
from app.api import router as api_router
from app.core.database import engine, Base
from app.core.scheduler import start_scheduler

load_dotenv()

# Global scheduler instance
scheduler = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    global scheduler

    # Startup
    async with engine.begin() as conn:
        # Create tables on startup (use alembic in production)
        await conn.run_sync(Base.metadata.create_all)

    # Start scheduled tasks
    scheduler = start_scheduler()

    yield

    # Shutdown
    if scheduler:
        scheduler.shutdown()
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Geron Mamasafe - Maternal, Neonatal, and Child Health AI Assistant",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Geron Mamasafe Health AI",
        "docs": "/docs",
        "api": "/api/v1",
    }
