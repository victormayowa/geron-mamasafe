"""
Mothers API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.models import Mother, HealthCenter, RiskLevel, PregnancyStage
from app.schemas.schemas import (
    Mother as MotherSchema,
    MotherCreate,
    MotherUpdate,
    PaginatedResponse,
    PaginationResponse
)
from app.services.risk_stratification import RiskStratificationService

router = APIRouter()


@router.post("/", response_model=MotherSchema, status_code=201)
async def create_mother(
    mother_data: MotherCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new mother"""
    
    # Check if phone number already exists
    existing = await db.execute(
        select(Mother).where(Mother.phone_number == mother_data.phone_number)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    # Create mother record
    mother = Mother(
        **mother_data.dict(exclude={'consent_given'}),
        consent_given=mother_data.consent_given,
        consent_date=datetime.utcnow() if mother_data.consent_given else None,
        is_registered=True
    )
    
    db.add(mother)
    await db.flush()
    await db.refresh(mother)
    
    # Assess risk
    risk_service = RiskStratificationService()
    risk_level, risk_factors, risk_description = await risk_service.assess_mother_risk(mother)
    
    await db.commit()
    await db.refresh(mother)
    
    return mother


@router.get("/", response_model=dict)
async def list_mothers(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    district: Optional[str] = None,
    risk_level: Optional[RiskLevel] = None,
    pregnancy_stage: Optional[PregnancyStage] = None,
    health_center_id: Optional[int] = None,
    is_high_risk: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all mothers with pagination and filters"""
    
    query = select(Mother)
    
    # Apply filters
    if district:
        query = query.where(Mother.district == district)
    if risk_level:
        query = query.where(Mother.risk_level == risk_level)
    if pregnancy_stage:
        query = query.where(Mother.pregnancy_stage == pregnancy_stage)
    if health_center_id:
        query = query.where(Mother.health_center_id == health_center_id)
    if is_high_risk is not None:
        query = query.where(Mother.is_high_risk == is_high_risk)
    
    # Get total count
    count_query = select(Mother)
    if district:
        count_query = count_query.where(Mother.district == district)
    if risk_level:
        count_query = count_query.where(Mother.risk_level == risk_level)
    if pregnancy_stage:
        count_query = count_query.where(Mother.pregnancy_stage == pregnancy_stage)
    if health_center_id:
        count_query = count_query.where(Mother.health_center_id == health_center_id)
    if is_high_risk is not None:
        count_query = count_query.where(Mother.is_high_risk == is_high_risk)
    
    count_result = await db.execute(count_query)
    total = len(count_result.scalars().all())
    
    # Apply pagination
    offset = (page - 1) * size
    query = query.offset(offset).limit(size)
    
    result = await db.execute(query)
    mothers = result.scalars().all()
    
    return {
        "success": True,
        "data": [MotherSchema.model_validate(m) for m in mothers],
        "pagination": {
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size
        }
    }


@router.get("/{mother_id}", response_model=MotherSchema)
async def get_mother(
    mother_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific mother by ID"""
    
    result = await db.execute(select(Mother).where(Mother.id == mother_id))
    mother = result.scalar_one_or_none()
    
    if not mother:
        raise HTTPException(status_code=404, detail="Mother not found")
    
    return mother


@router.put("/{mother_id}", response_model=MotherSchema)
async def update_mother(
    mother_id: int,
    mother_data: MotherUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update mother information"""
    
    result = await db.execute(select(Mother).where(Mother.id == mother_id))
    mother = result.scalar_one_or_none()
    
    if not mother:
        raise HTTPException(status_code=404, detail="Mother not found")
    
    # Update fields
    update_data = mother_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(mother, field, value)
    
    # Re-assess risk if relevant fields changed
    if any(field in update_data for field in ['age', 'gravida', 'parity', 'previous_complications', 
                                               'blood_group', 'chronic_conditions', 'pregnancy_stage']):
        risk_service = RiskStratificationService()
        risk_level, risk_factors, risk_description = await risk_service.assess_mother_risk(mother)
    
    await db.commit()
    await db.refresh(mother)
    
    return mother


@router.get("/{mother_id}/risk-assessment")
async def assess_mother_risk(
    mother_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get risk assessment for a mother"""
    
    result = await db.execute(select(Mother).where(Mother.id == mother_id))
    mother = result.scalar_one_or_none()
    
    if not mother:
        raise HTTPException(status_code=404, detail="Mother not found")
    
    risk_service = RiskStratificationService()
    risk_level, risk_factors, risk_description = await risk_service.assess_mother_risk(mother)
    
    await db.commit()
    
    return {
        "mother_id": mother.id,
        "risk_level": risk_level.value,
        "is_high_risk": mother.is_high_risk,
        "risk_factors": risk_factors,
        "risk_description": risk_description,
        "recommendations": RiskStratificationService.get_risk_recommendations(risk_level, is_mother=True)
    }


@router.get("/search/phone/{phone_number}")
async def search_mother_by_phone(
    phone_number: str,
    db: AsyncSession = Depends(get_db)
):
    """Search for mother by phone number"""
    
    result = await db.execute(
        select(Mother).where(
            or_(
                Mother.phone_number == phone_number,
                Mother.whatsapp_number == phone_number
            )
        )
    )
    mother = result.scalar_one_or_none()
    
    if not mother:
        raise HTTPException(status_code=404, detail="Mother not found")
    
    return mother
