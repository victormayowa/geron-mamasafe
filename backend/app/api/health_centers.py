"""
Health Centers API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.core.database import get_db
from app.models.models import HealthCenter, FacilityLevel
from app.schemas.schemas import HealthCenter as HealthCenterSchema, HealthCenterCreate

router = APIRouter()


@router.post("/", response_model=HealthCenterSchema, status_code=201)
async def create_health_center(
    center_data: HealthCenterCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new health center"""
    
    # Check if code already exists
    existing = await db.execute(
        select(HealthCenter).where(HealthCenter.code == center_data.code)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Health center code already exists")
    
    center = HealthCenter(**center_data.dict())
    db.add(center)
    await db.commit()
    await db.refresh(center)
    
    return center


@router.get("/")
async def list_health_centers(
    district: Optional[str] = None,
    facility_level: Optional[FacilityLevel] = None,
    state: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all health centers with filters"""
    
    query = select(HealthCenter).where(HealthCenter.is_active == True)
    
    if district:
        query = query.where(HealthCenter.district == district)
    if facility_level:
        query = query.where(HealthCenter.facility_level == facility_level)
    if state:
        query = query.where(HealthCenter.state == state)
    
    result = await db.execute(query)
    centers = result.scalars().all()
    
    return {
        "success": True,
        "data": [HealthCenterSchema.model_validate(c) for c in centers]
    }


@router.get("/{center_id}", response_model=HealthCenterSchema)
async def get_health_center(
    center_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get health center details"""
    
    result = await db.execute(
        select(HealthCenter).where(HealthCenter.id == center_id)
    )
    center = result.scalar_one_or_none()
    
    if not center:
        raise HTTPException(status_code=404, detail="Health center not found")
    
    return center
