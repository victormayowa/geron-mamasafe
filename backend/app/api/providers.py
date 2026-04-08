"""
Health Providers API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_password_hash, create_access_token, verify_password
from app.models.models import HealthProvider
from app.schemas.schemas import (
    HealthProvider as HealthProviderSchema,
    HealthProviderCreate,
    HealthProviderLogin
)

router = APIRouter()


@router.post("/register", response_model=HealthProviderSchema, status_code=201)
async def register_provider(
    provider_data: HealthProviderCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new health provider"""
    
    # Check if email already exists
    existing = await db.execute(
        select(HealthProvider).where(HealthProvider.email == provider_data.email)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create provider
    provider = HealthProvider(
        **provider_data.dict(exclude={'password'}),
        password_hash=get_password_hash(provider_data.password)
    )
    
    db.add(provider)
    await db.commit()
    await db.refresh(provider)
    
    return provider


@router.post("/login")
async def login_provider(
    login_data: HealthProviderLogin,
    db: AsyncSession = Depends(get_db)
):
    """Login health provider"""
    
    result = await db.execute(
        select(HealthProvider).where(HealthProvider.email == login_data.email)
    )
    provider = result.scalar_one_or_none()
    
    if not provider or not verify_password(login_data.password, provider.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not provider.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")
    
    # Update last login
    provider.last_login = datetime.utcnow()
    await db.commit()
    
    # Create access token
    access_token = create_access_token(
        data={"sub": provider.email, "provider_id": provider.id}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "provider": HealthProviderSchema.model_validate(provider)
    }


@router.get("/{provider_id}", response_model=HealthProviderSchema)
async def get_provider(
    provider_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get health provider details"""
    
    result = await db.execute(
        select(HealthProvider).where(HealthProvider.id == provider_id)
    )
    provider = result.scalar_one_or_none()
    
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    
    return provider
