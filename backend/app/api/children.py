"""
Children API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import datetime

from app.core.database import get_db
from app.models.models import Child, Mother, ChildAgeGroup
from app.schemas.schemas import Child as ChildSchema, ChildCreate
from app.services.risk_stratification import RiskStratificationService

router = APIRouter()


@router.post("/", response_model=ChildSchema, status_code=201)
async def register_child(
    child_data: ChildCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new child"""
    
    # Verify mother exists
    mother_result = await db.execute(
        select(Mother).where(Mother.id == child_data.mother_id)
    )
    mother = mother_result.scalar_one_or_none()
    
    if not mother:
        raise HTTPException(status_code=404, detail="Mother not found")
    
    # Calculate age group from date of birth
    dob = child_data.date_of_birth
    now = datetime.utcnow()
    age_days = (now - dob).days
    
    if age_days <= 28:
        age_group = ChildAgeGroup.NEWBORN
    elif age_days <= 365:
        age_group = ChildAgeGroup.INFANT
    elif age_days <= 1095:  # 3 years
        age_group = ChildAgeGroup.TODDLER
    elif age_days <= 1825:  # 5 years
        age_group = ChildAgeGroup.PRESCHOOL
    else:
        age_group = None  # Over 5 years
    
    # Create child
    child = Child(
        **child_data.dict(),
        age_group=age_group
    )
    
    db.add(child)
    await db.flush()
    await db.refresh(child)
    
    # Assess risk
    risk_service = RiskStratificationService()
    risk_level, risk_factors, risk_description = await risk_service.assess_child_risk(child, mother)
    
    await db.commit()
    await db.refresh(child)
    
    return child


@router.get("/{child_id}", response_model=ChildSchema)
async def get_child(
    child_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get child details"""
    
    result = await db.execute(select(Child).where(Child.id == child_id))
    child = result.scalar_one_or_none()
    
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    
    return child


@router.get("/mother/{mother_id}")
async def get_mother_children(
    mother_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all children for a mother"""
    
    result = await db.execute(
        select(Child)
        .where(Child.mother_id == mother_id)
        .where(Child.is_active == True)
    )
    children = result.scalars().all()
    
    return {
        "success": True,
        "data": [ChildSchema.model_validate(c) for c in children]
    }


@router.get("/{child_id}/risk-assessment")
async def assess_child_risk(
    child_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get risk assessment for a child"""
    
    result = await db.execute(select(Child).where(Child.id == child_id))
    child = result.scalar_one_or_none()
    
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    
    # Get mother
    mother_result = await db.execute(select(Mother).where(Mother.id == child.mother_id))
    mother = mother_result.scalar_one_or_none()
    
    risk_service = RiskStratificationService()
    risk_level, risk_factors, risk_description = await risk_service.assess_child_risk(child, mother)
    
    await db.commit()
    
    return {
        "child_id": child.id,
        "risk_level": risk_level.value,
        "is_high_risk": child.is_high_risk,
        "risk_factors": risk_factors,
        "risk_description": risk_description,
        "recommendations": RiskStratificationService.get_risk_recommendations(risk_level, is_mother=False)
    }
