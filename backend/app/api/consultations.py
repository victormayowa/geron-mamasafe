"""
AI Consultations API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.core.database import get_db
from app.models.models import Mother, Consultation, RiskLevel
from app.schemas.schemas import ConsultationQuery, Consultation as ConsultationSchema
from app.services.ai_consultation import AIConsultationService

router = APIRouter()


@router.post("/query", response_model=dict)
async def submit_query(
    query_data: ConsultationQuery,
    db: AsyncSession = Depends(get_db)
):
    """Submit a health-related question to the AI"""
    
    # Find mother
    result = await db.execute(
        select(Mother).where(
            (Mother.phone_number == query_data.phone_number) |
            (Mother.whatsapp_number == query_data.phone_number)
        )
    )
    mother = result.scalar_one_or_none()
    
    if not mother:
        raise HTTPException(status_code=404, detail="Mother not found. Please register at your health center first.")
    
    # Process query
    consultation_service = AIConsultationService()
    
    mother_profile = {
        "pregnancy_stage": mother.pregnancy_stage.value if mother.pregnancy_stage else None,
        "risk_level": mother.risk_level.value if mother.risk_level else None
    }
    
    result = await consultation_service.process_query(
        query_data.query,
        mother_profile=mother_profile
    )
    
    # Save consultation
    consultation = Consultation(
        mother_id=mother.id,
        query=query_data.query,
        response=result["response"],
        category=result["category"],
        urgency_level=result["urgency_level"],
        ai_confidence=result["ai_confidence"],
        requires_follow_up=result["requires_follow_up"],
        escalated=result["escalated"]
    )
    
    db.add(consultation)
    await db.commit()
    await db.refresh(consultation)
    
    return {
        "success": True,
        "response": result["response"],
        "urgency_level": result["urgency_level"].value if result["urgency_level"] else None,
        "category": result["category"],
        "requires_follow_up": result["requires_follow_up"]
    }


@router.get("/history/{mother_id}")
async def get_consultation_history(
    mother_id: int,
    page: int = 1,
    size: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """Get consultation history for a mother"""
    
    result = await db.execute(
        select(Consultation)
        .where(Consultation.mother_id == mother_id)
        .order_by(Consultation.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
    )
    
    consultations = result.scalars().all()
    
    return {
        "success": True,
        "data": [ConsultationSchema.model_validate(c) for c in consultations],
        "pagination": {
            "page": page,
            "size": size
        }
    }
